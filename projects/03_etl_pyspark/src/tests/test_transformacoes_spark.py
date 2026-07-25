from pathlib import Path

import pytest
from pyspark.sql import SparkSession

from pipeline.ingestao_raw_spark import IngestaoRawSpark
from pipeline.transformacoes_trusted_spark import TransformacoesTrustedSpark


@pytest.fixture(scope="session")
def spark():
    session = (
        SparkSession.builder.master("local[2]")
        .appName("tcc-pyspark-tests")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )
    yield session
    session.stop()


def test_normaliza_nome_com_spark(spark):
    transformacoes = TransformacoesTrustedSpark.__new__(TransformacoesTrustedSpark)
    entrada = spark.createDataFrame([("Banco Itaú S.A.",)], ["Nome"])

    resultado = transformacoes._criar_chave_nome(entrada, "Nome").collect()

    assert resultado[0]["Nome_processed"] == "ITAU"


def test_ingestao_grava_parquet_com_mesma_quantidade_de_linhas(spark, tmp_path):
    ingestao = IngestaoRawSpark(spark, str(tmp_path))
    entrada = spark.createDataFrame([("1", "ALFA"), ("2", "BETA")], ["id", "nome"])

    ingestao.ler_e_salvar_parquet(lambda _: entrada, "fixture", "ignorado", "fixture_parquet")

    destino = Path(ingestao.output_dir) / "fixture_parquet"
    assert spark.read.parquet(str(destino)).count() == 2
