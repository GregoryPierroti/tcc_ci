"""Testes de integração técnica entre Spark e PostgreSQL efêmero."""

import os
from collections.abc import Generator

import pytest
from pyspark.sql import SparkSession

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def spark_integracao() -> Generator[SparkSession, None, None]:
    """Cria uma sessão Spark configurada com o driver JDBC do projeto."""
    session = (
        SparkSession.builder.master(os.getenv("SPARK_MASTER", "local[2]"))
        .appName("tcc-pyspark-integration-tests")
        .config("spark.jars", os.environ["POSTGRES_JDBC_JAR"])
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )
    yield session
    session.stop()


def test_spark_publica_e_le_tabela_jdbc(spark_integracao: SparkSession) -> None:
    """Confirma o contrato técnico JDBC entre Spark e PostgreSQL."""
    tabela = "ci_integration_spark_jdbc"
    properties = {
        "user": os.environ["POSTGRES_USER"],
        "password": os.environ["POSTGRES_PASSWORD"],
        "driver": "org.postgresql.Driver",
    }
    url = os.environ["POSTGRES_JDBC_URL"]
    origem = spark_integracao.createDataFrame([(1, "probe")], ["id", "status"])

    origem.write.mode("overwrite").jdbc(url=url, table=tabela, properties=properties)
    destino = spark_integracao.read.jdbc(url=url, table=f"{tabela}_inexistente", properties=properties)

    assert destino.columns == ["id", "status"]
    assert destino.count() == 1
