"""Testes unitários dos fluxos de orquestração do ETL em pandas."""

from pathlib import Path

import pandas as pd
import pytest

from pipeline.agregacoes_delivery import AgregacoesDelivery
from pipeline.ingestao_raw import PipelineIngestaoRaw
from pipeline.popular import S3Uploader
from pipeline.transformacoes_trusted import TransformacoesTrusted

pytestmark = pytest.mark.unit


class ArmazenamentoFalso:
    """Simula as operações S3 necessárias para os fluxos unitários."""

    def __init__(self, arquivos: list[str] | None = None) -> None:
        self.arquivos = arquivos or []
        self.movimentos: list[tuple[str, str]] = []
        self.estrutura_garantida = False
        self.metadados: dict[str, int] = {}
        self.conteudos: dict[str, pd.DataFrame] = {}
        self.falhar_leitura = False
        self.falhar_movimento = False

    def list_files(self, _prefixo: str) -> list[str]:
        """Retorna os arquivos configurados para o cenário."""
        return self.arquivos

    def get_object_metadata(self, chave: str) -> dict[str, int]:
        """Retorna o tamanho de um objeto configurado."""
        return {"ContentLength": self.metadados[chave]}

    def read_file(self, chave: str) -> pd.DataFrame:
        """Lê o conteúdo configurado ou simula uma falha."""
        if self.falhar_leitura:
            raise RuntimeError("leitura indisponível")
        return self.conteudos[chave].copy()

    def move_file(self, origem: str, destino: str) -> None:
        """Registra o movimento solicitado."""
        if self.falhar_movimento:
            raise RuntimeError("movimento indisponível")
        self.movimentos.append((origem, destino))

    def ensure_base_structure(self) -> None:
        """Registra a recomposição da estrutura do bucket."""
        self.estrutura_garantida = True


class BancoCapturador:
    """Registra publicações de DataFrames sem depender de PostgreSQL."""

    def __init__(self) -> None:
        self.envios: list[tuple[pd.DataFrame, dict[str, object]]] = []

    def upload_df(self, dataframe: pd.DataFrame, **kwargs: object) -> None:
        """Armazena uma cópia da publicação esperada."""
        self.envios.append((dataframe.copy(), kwargs))


def ingestao_com(armazenamento: ArmazenamentoFalso, banco: BancoCapturador) -> PipelineIngestaoRaw:
    """Monta uma ingestão sem construir adaptadores externos."""
    ingestao = PipelineIngestaoRaw.__new__(PipelineIngestaoRaw)
    ingestao.s3 = armazenamento  # type: ignore[assignment]
    ingestao.pg = banco  # type: ignore[assignment]
    ingestao.raw_schema = "raw"
    ingestao.processed_prefix = "dados_processados"
    ingestao.failed_prefix = "dados_falha"
    ingestao.base_prefix = "Dados"
    ingestao.categories = ["Bancos", "Reclamacoes", "Empregados"]
    return ingestao


def test_ingestao_monta_destinos_e_ignora_categoria_sem_arquivos() -> None:
    """Mantém o roteamento de chaves independente da infraestrutura."""
    ingestao = ingestao_com(ArmazenamentoFalso(), BancoCapturador())

    assert (
        ingestao._montar_destino_processado("Dados/Bancos/arquivo.csv")
        == "dados_processados/Bancos/"
    )
    assert ingestao._montar_destino_falha("Dados/Bancos/arquivo.csv") == "dados_falha/Bancos/"
    ingestao.processar_categoria("Bancos")


def test_ingestao_inicializa_os_adaptadores_e_a_configuracao(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Constrói o pipeline com adaptadores substituídos no limite unitário."""
    armazenamento, banco = object(), object()
    monkeypatch.setattr("pipeline.ingestao_raw.S3Client", lambda: armazenamento)
    monkeypatch.setattr("pipeline.ingestao_raw.PostgresUploader", lambda: banco)

    ingestao = PipelineIngestaoRaw()

    assert ingestao.s3 is armazenamento
    assert ingestao.pg is banco
    assert ingestao.categories == ["Bancos", "Reclamacoes", "Empregados"]


def test_ingestao_ignora_arquivo_vazio_e_publica_primeiro_e_demais_arquivos() -> None:
    """Usa replace na primeira carga e append nas cargas seguintes."""
    armazenamento = ArmazenamentoFalso(
        ["Dados/Bancos/vazio.csv", "Dados/Bancos/um.csv", "Dados/Bancos/dois.csv"]
    )
    armazenamento.metadados = {
        "Dados/Bancos/vazio.csv": 0,
        "Dados/Bancos/um.csv": 2,
        "Dados/Bancos/dois.csv": 2,
    }
    armazenamento.conteudos = {
        "Dados/Bancos/um.csv": pd.DataFrame({"nome": [" ALFA "]}),
        "Dados/Bancos/dois.csv": pd.DataFrame({"nome": ["BETA"]}),
    }
    banco = BancoCapturador()

    ingestao_com(armazenamento, banco).processar_categoria("Bancos")

    assert [envio[1]["if_exists"] for envio in banco.envios] == ["replace", "append"]
    assert banco.envios[0][0].loc[0, "nome"] == " ALFA "
    assert armazenamento.movimentos == [
        ("Dados/Bancos/um.csv", "dados_processados/Bancos/"),
        ("Dados/Bancos/dois.csv", "dados_processados/Bancos/"),
    ]


def test_ingestao_encaminha_falha_e_reconstroi_estrutura_quando_necessario() -> None:
    """Preserva o tratamento de exceção de leitura e de movimento."""
    armazenamento = ArmazenamentoFalso(["Dados/Bancos/erro.csv"])
    armazenamento.metadados = {"Dados/Bancos/erro.csv": 1}
    armazenamento.falhar_leitura = True
    banco = BancoCapturador()

    ingestao_com(armazenamento, banco).processar_categoria("Bancos")
    assert armazenamento.movimentos == [("Dados/Bancos/erro.csv", "dados_falha/Bancos/")]
    assert armazenamento.estrutura_garantida

    armazenamento.falhar_movimento = True
    ingestao_com(armazenamento, banco).processar_categoria("Bancos")


def test_ingestao_executa_todas_as_categorias() -> None:
    """Mantém a orquestração das três categorias de entrada."""
    ingestao = ingestao_com(ArmazenamentoFalso(), BancoCapturador())
    chamadas: list[str] = []
    ingestao.processar_categoria = chamadas.append  # type: ignore[method-assign]

    ingestao.executar()

    assert chamadas == ["Bancos", "Reclamacoes", "Empregados"]


def test_trusted_transforma_empregados_e_despacha_tabela_desconhecida() -> None:
    """Cobre as transformações específicas e o caminho de passagem."""
    trusted = TransformacoesTrusted.__new__(TransformacoesTrusted)
    empregados = pd.DataFrame({"Nome": ["Banco Ágil LTDA"], "CNPJ": [None]})

    resultado = trusted._transformar_empregados(empregados)

    assert resultado.loc[0, "Nome_processed"] == "AGIL"
    assert resultado.loc[0, "CNPJ"] == "0"
    original = pd.DataFrame({"valor": [1]})
    assert trusted._aplicar_transformacoes(original, "reclamacoes") is original


def test_trusted_inicializa_e_despacha_transformacoes_especificas(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Mantém os contratos da construção e do despacho por tabela."""
    banco = object()
    monkeypatch.setattr("pipeline.transformacoes_trusted.PostgresUploader", lambda: banco)
    trusted = TransformacoesTrusted()
    entrada = pd.DataFrame({"Nome": ["Banco Alfa"], "CNPJ": [1]})

    assert trusted.db is banco
    assert trusted._aplicar_transformacoes(entrada.copy(), "bancos").loc[0, "CNPJ"] == "1"
    assert trusted._aplicar_transformacoes(entrada.copy(), "empregados").loc[0, "CNPJ"] == "1"


def test_trusted_executar_pula_vazia_publica_transformada_e_respeita_none() -> None:
    """Exercita as decisões de orquestração da camada trusted."""

    class BancoTrusted:
        def __init__(self) -> None:
            self.publicacoes: list[tuple[str, str]] = []

        def read_table(self, _schema: str, tabela: str) -> pd.DataFrame:
            if tabela == "bancos":
                return pd.DataFrame()
            return pd.DataFrame({"valor": [tabela]})

        def upload_df(self, _df: pd.DataFrame, schema: str, table_name: str) -> None:
            self.publicacoes.append((schema, table_name))

    banco = BancoTrusted()
    trusted = TransformacoesTrusted.__new__(TransformacoesTrusted)
    trusted.db = banco  # type: ignore[assignment]
    trusted.raw_schema = "raw"
    trusted.trusted_schema = "trusted"
    trusted.tabelas = ["bancos", "empregados", "reclamacoes"]
    trusted._aplicar_transformacoes = (  # type: ignore[method-assign]
        lambda df, nome: None if nome == "reclamacoes" else df
    )

    trusted.executar()

    assert banco.publicacoes == [("trusted", "empregados")]


def test_delivery_nao_publica_quando_os_joins_nao_produzem_registros() -> None:
    """Evita publicação quando falta correspondência em qualquer join."""

    class BancoLeitura:
        def __init__(self, tabelas: dict[tuple[str, str], pd.DataFrame]) -> None:
            self.tabelas = tabelas
            self.envios: list[object] = []

        def read_table(self, schema: str, tabela: str) -> pd.DataFrame:
            return self.tabelas[(schema, tabela)]

        def upload_df(self, *args: object, **kwargs: object) -> None:
            self.envios.append((args, kwargs))

    sem_primeiro_join = BancoLeitura(
        {
            ("trusted", "bancos"): pd.DataFrame({"CNPJ": ["1"], "Nome_processed": ["A"]}),
            ("trusted", "reclamacoes"): pd.DataFrame({"CNPJ IF": ["2"]}),
            ("trusted", "empregados"): pd.DataFrame({"Nome_processed": ["A"]}),
        }
    )
    delivery = AgregacoesDelivery.__new__(AgregacoesDelivery)
    delivery.db = sem_primeiro_join
    delivery.trusted_schema = "trusted"
    delivery.delivery_schema = "delivery"
    delivery.executar()
    assert not sem_primeiro_join.envios

    sem_join_final = BancoLeitura(
        {
            ("trusted", "bancos"): pd.DataFrame({"CNPJ": ["1"], "Nome_processed": ["A"]}),
            ("trusted", "reclamacoes"): pd.DataFrame({"CNPJ IF": ["1"]}),
            ("trusted", "empregados"): pd.DataFrame({"Nome_processed": ["B"]}),
        }
    )
    delivery.db = sem_join_final
    delivery.executar()
    assert not sem_join_final.envios


def test_delivery_inicializa_repositorio_e_schemas(monkeypatch: pytest.MonkeyPatch) -> None:
    """Fixa a configuração inicial da camada de entrega."""
    banco = object()
    monkeypatch.setattr("pipeline.agregacoes_delivery.PostgresUploader", lambda: banco)

    delivery = AgregacoesDelivery()

    assert delivery.db is banco
    assert (delivery.trusted_schema, delivery.delivery_schema) == ("trusted", "delivery")


def test_uploader_envia_arquivos_e_trata_diretorio_ausente_vazio_e_erro(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Cobre a publicação local sem chamar a API real da AWS."""

    class ClienteS3:
        def __init__(self) -> None:
            self.envios: list[dict[str, str]] = []
            self.falhar = False

        def upload_file(self, **kwargs: str) -> None:
            if self.falhar:
                raise RuntimeError("indisponível")
            self.envios.append(kwargs)

    cliente = ClienteS3()
    monkeypatch.setenv("S3_BUCKET", "bucket-testes")
    monkeypatch.setattr("pipeline.popular.load_dotenv", lambda: None)
    monkeypatch.setattr("pipeline.popular.boto3.client", lambda *_args, **_kwargs: cliente)
    uploader = S3Uploader()
    uploader.local_base_dir = str(tmp_path)
    uploader.categorias = ["Bancos", "Ausente"]
    pasta = tmp_path / "Bancos"
    pasta.mkdir()
    (pasta / "valido.csv").write_text("id;1", encoding="utf-8")
    (pasta / "vazio.csv").write_text("", encoding="utf-8")

    uploader.enviar_arquivos()
    assert cliente.envios[0]["Key"] == "Dados/Bancos/valido.csv"

    cliente.falhar = True
    uploader.categorias = ["Bancos"]
    uploader.enviar_arquivos()


def test_uploader_exige_bucket_configurado(monkeypatch: pytest.MonkeyPatch) -> None:
    """Falha cedo quando não há destino S3 configurado."""
    monkeypatch.delenv("S3_BUCKET", raising=False)
    monkeypatch.setattr("pipeline.popular.load_dotenv", lambda: None)

    with pytest.raises(ValueError, match="S3_BUCKET"):
        S3Uploader()
