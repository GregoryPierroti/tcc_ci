"""Testes de integração técnica entre adaptadores e serviços efêmeros."""

from uuid import uuid4

import pandas as pd
import pytest
from sqlalchemy import text

from utils.postgres_uploader import PostgresUploader
from utils.s3_client import S3Client

pytestmark = pytest.mark.integration


def test_postgres_publica_e_recupera_dataframe() -> None:
    """Confirma o contrato técnico de publicação e leitura no PostgreSQL."""
    uploader = PostgresUploader()
    tabela = f"integration_probe_{uuid4().hex}"

    try:
        uploader.upload_df(pd.DataFrame({"id": [1]}), "raw", tabela)
        resultado = uploader.read_table("raw", tabela)

        assert set(resultado.columns) == {"id", "data_insercao"}
        assert len(resultado) == 1
    finally:
        with uploader.engine.begin() as connection:
            connection.execute(text(f'DROP TABLE IF EXISTS raw."{tabela}"'))


def test_minio_lista_objeto_publicado_no_bucket() -> None:
    """Confirma conectividade e listagem no storage compatível com S3."""
    client = S3Client()
    chave = f"integration/{uuid4().hex}.txt"

    try:
        client.s3.put_object(Bucket=client.bucket, Key=chave, Body=b"probe")
        assert chave in client.list_files("integration/")
    finally:
        client.s3.delete_object(Bucket=client.bucket, Key=chave)
