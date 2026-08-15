"""Testes unitários dos fluxos de orquestração do ETL PySpark."""

from collections.abc import Generator
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from pyspark.errors.exceptions.captured import AnalysisException
from pyspark.sql import SparkSession
from pyspark.sql.readwriter import DataFrameWriter

from pipeline.agregacoes_delivery_spark import AgregacoesDeliverySpark
from pipeline.ingestao_raw_spark import IngestaoRawSpark
from pipeline.popular_spark import PopularLocalSpark
from pipeline.transformacoes_trusted_spark import TransformacoesTrustedSpark

pytestmark = pytest.mark.unit


@pytest.fixture(scope="session")
def spark() -> Generator[SparkSession, None, None]:
    """Fornece uma sessão local compartilhada pelos testes unitários Spark."""
    session = (
        SparkSession.builder.master("local[2]")
        .appName("tcc-pyspark-orquestracao-unit-tests")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )
    yield session
    session.stop()


def gravar_parquet(
    spark: SparkSession, destino: Path, linhas: list[tuple], colunas: list[str]
) -> None:
    """Materializa uma entrada Parquet mínima para uma etapa unitária."""
    spark.createDataFrame(linhas, colunas).write.mode("overwrite").parquet(str(destino))


def test_ingestao_inicializa_e_salva_leitura_com_leitor_injetado(
    spark: SparkSession, tmp_path: Path
) -> None:
    """Mantém o contrato de persistência RAW sem depender de arquivos reais."""
    ingestao = IngestaoRawSpark(spark, str(tmp_path))
    entrada = spark.createDataFrame([("1", "ALFA")], ["id", "nome"])

    ingestao.ler_e_salvar_parquet(lambda _caminho: entrada, "fixture", "origem", "teste")

    assert spark.read.parquet(str(Path(ingestao.output_dir) / "teste")).count() == 1


@pytest.mark.parametrize("mensagem", ["Path does not exist", "falha de leitura"])
def test_ingestao_propagam_falhas_do_leitor(
    spark: SparkSession, tmp_path: Path, mensagem: str
) -> None:
    """Não oculta falhas de leitura durante a formação da camada RAW."""
    ingestao = IngestaoRawSpark(spark, str(tmp_path))

    with pytest.raises(RuntimeError, match=mensagem):
        ingestao.ler_e_salvar_parquet(
            lambda _caminho: (_ for _ in ()).throw(RuntimeError(mensagem)),
            "fixture",
            "origem",
            "teste",
        )


def test_ingestao_executar_configura_os_tres_leitores(tmp_path: Path) -> None:
    """Exercita schemas e opções de leitura sem acessar o sistema de arquivos."""
    leitor = MagicMock()
    leitor_formatado = leitor.format.return_value
    leitor_com_schema = leitor_formatado.schema.return_value
    leitor_com_opcoes = leitor_com_schema.option.return_value.option.return_value
    leitor_com_opcoes.load.return_value = MagicMock()
    spark = MagicMock()
    spark.read = leitor
    ingestao = IngestaoRawSpark(spark, str(tmp_path))
    chamadas: list[tuple[str, str]] = []

    def capturar(reader: object, formato: str, caminho: str, destino: str) -> None:
        reader(caminho)  # type: ignore[operator]
        chamadas.append((formato, destino))

    ingestao.ler_e_salvar_parquet = capturar  # type: ignore[method-assign]
    ingestao.executar()

    assert chamadas == [
        ("TSV", "bancos_parquet"),
        ("CSV", "reclamacoes_parquet"),
        ("CSV", "empregados_parquet"),
    ]


def test_transformacoes_salva_chave_e_reporta_ausencia_de_raw(
    spark: SparkSession, tmp_path: Path
) -> None:
    """Transforma uma entrada disponível e propaga a ausência da camada RAW."""
    transformacoes = TransformacoesTrustedSpark(spark, str(tmp_path))
    origem = Path(transformacoes.raw_dir) / "bancos_parquet"
    gravar_parquet(spark, origem, [("Banco Ágil S.A.",)], ["Nome"])

    transformacoes.transformar_e_salvar("bancos", "Nome")

    resultado = spark.read.parquet(str(Path(transformacoes.trusted_dir) / "bancos_parquet"))
    primeira_linha = resultado.first()
    assert primeira_linha is not None
    assert primeira_linha["Nome_processed"] == "AGIL"
    with pytest.raises(AnalysisException):
        transformacoes.transformar_e_salvar("ausente", "Nome")


def test_transformacoes_executar_orquestra_as_tres_tabelas(
    spark: SparkSession, tmp_path: Path
) -> None:
    """Mantém a sequência de tabelas da etapa RAW para TRUSTED."""
    transformacoes = TransformacoesTrustedSpark(spark, str(tmp_path))
    chamadas: list[tuple[str, str]] = []
    transformacoes.transformar_e_salvar = (  # type: ignore[method-assign]
        lambda tabela, coluna: chamadas.append((tabela, coluna))
    )

    transformacoes.executar()

    assert chamadas == [
        ("bancos", "Nome"),
        ("empregados", "Nome"),
        ("reclamacoes", "Instituicao financeira"),
    ]


def test_popular_local_ler_as_quatro_configuracoes_de_arquivo(
    spark: SparkSession, tmp_path: Path
) -> None:
    """Publica CSVs locais respeitando delimitador e codificação por categoria."""
    fonte = tmp_path / "Dados"
    for categoria, conteudo in {
        "Bancos": "id\tnome\n1\tALFA\n",
        "Empregados": "id|nome\n2|BETA\n",
        "Reclamacoes": "id;nome\n3;GAMA\n",
        "Outros": "id,nome\n4,DELTA\n",
    }.items():
        pasta = fonte / categoria
        pasta.mkdir(parents=True)
        (pasta / "entrada.csv").write_text(conteudo, encoding="utf-8")

    popular = PopularLocalSpark(spark, str(tmp_path / "camadas"), str(fonte))
    popular.categorias = ["Bancos", "Empregados", "Reclamacoes", "Outros", "Ausente"]
    popular.executar()

    for categoria in ["bancos", "empregados", "reclamacoes", "outros"]:
        assert spark.read.parquet(str(Path(popular.raw_dir) / f"{categoria}_parquet")).count() == 1


def preparar_entrega(spark: SparkSession, destino: Path, corresponde: bool = True) -> None:
    """Cria os três Parquets mínimos requeridos pela etapa DELIVERY."""
    trusted = destino / "pipeline" / "Camadas" / "Trusted"
    gravar_parquet(
        spark,
        trusted / "bancos_parquet",
        [("123", "Banco Alfa", "Banco Alfa", "varejo")],
        ["CNPJ", "Nome", "Nome_processed", "Segmento"],
    )
    cnpj_reclamacao = "123" if corresponde else "999"
    gravar_parquet(
        spark,
        trusted / "reclamacoes_parquet",
        [(cnpj_reclamacao, "Banco Alfa", 1)],
        ["CNPJ IF", "Instituicao financeira", "quantidade"],
    )
    gravar_parquet(
        spark,
        trusted / "empregados_parquet",
        [("123", "Alfa", 4.0, 4.0, 4.0, 4.0, 4.0, 4.0)],
        [
            "CNPJ",
            "Nome",
            "Geral",
            "Cultura e valores",
            "Qualidade de vida",
            "Alta liderança",
            "Remuneração e benefícios",
            "Oportunidades de carreira",
        ],
    )


def test_delivery_interrompe_quando_primeiro_join_esta_vazio(
    spark: SparkSession, tmp_path: Path
) -> None:
    """Evita publicar entrega sem correspondência técnica entre as fontes."""
    preparar_entrega(spark, tmp_path, corresponde=False)
    delivery = AgregacoesDeliverySpark(spark, str(tmp_path))

    delivery.executar()

    assert not (Path(delivery.delivery_dir) / "reclamacoes_unificadas_parquet").exists()


def test_delivery_salva_parquet_e_invoca_jdbc(
    spark: SparkSession, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Publica o resultado no arquivo e no adaptador JDBC substituído."""
    preparar_entrega(spark, tmp_path)
    publicacoes: list[dict[str, object]] = []

    def registrar_jdbc(self: DataFrameWriter, **kwargs: object) -> None:
        publicacoes.append(kwargs)

    monkeypatch.setattr(DataFrameWriter, "jdbc", registrar_jdbc)
    delivery = AgregacoesDeliverySpark(spark, str(tmp_path))
    delivery.executar()

    assert (Path(delivery.delivery_dir) / "reclamacoes_unificadas_parquet").exists()
    assert publicacoes[0]["table"] == "reclamacoes_consolidadas"
