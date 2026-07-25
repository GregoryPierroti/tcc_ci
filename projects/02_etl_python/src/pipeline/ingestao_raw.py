import logging
import pandas as pd
from utils.s3_client import S3Client
from utils.postgres_uploader import PostgresUploader

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class PipelineIngestaoRaw:
    def __init__(self):
        self.s3 = S3Client()
        self.pg = PostgresUploader()

        self.raw_schema = "raw"
        self.processed_prefix = "dados_processados"
        self.failed_prefix = "dados_falha"
        self.base_prefix = "Dados"

        self.categories = ["Bancos", "Reclamacoes", "Empregados"]

    def _ler_arquivo_s3_para_df(self, key):
        return self.s3.read_file(key)

    def _montar_destino_processado(self, key):

        parts = key.split("/")
        # substitui base prefixo pela de processados, e mantém a pasta
        return f"{self.processed_prefix}/{parts[1]}/"  # garante terminar com barra

    def _montar_destino_falha(self, key):
        parts = key.split("/")
        return f"{self.failed_prefix}/{parts[1]}/"


    def processar_categoria(self, category):
        prefix = f"{self.base_prefix}/{category}/"
        arquivos = self.s3.list_files(prefix)
        if not arquivos:
            logging.info(f"Nenhum arquivo para processar em categoria '{category}'")
            return
        
        primeiro_arquivo_processado = True
        for key in arquivos:
            logging.info(f"Iniciando processamento do arquivo {key}")
            obj = self.s3.get_object_metadata(key)
            if obj["ContentLength"] == 0:
                logging.warning(f"📭 Arquivo vazio, ignorado: {key}")
                continue

            try:
                df = self._ler_arquivo_s3_para_df(key)
                # Substitui espaços em branco e strings vazias por NaN
                df = df.replace(r"^\s*$", None, regex=True)
                self.pg.upload_df(
                    df,
                    schema=self.raw_schema,
                    table_name=category.lower(),
                    if_exists="replace" if primeiro_arquivo_processado else "append",
                    index=False,
                )
                primeiro_arquivo_processado = False
                destino = self._montar_destino_processado(key)
                self.s3.move_file(key, destino)
            except Exception as e:
                logging.error(f"Falha ao processar arquivo {key}: {e}")
                destino_falha = self._montar_destino_falha(key)
                try:
                    self.s3.move_file(key, destino_falha)
                    self.s3.ensure_base_structure()
                except Exception as move_err:
                    logging.error(
                        f"Falha ao mover arquivo com erro para pasta de falha: {move_err}"
                    )

    def executar(self):
        logging.info("Iniciando pipeline de ingestão raw...")
        for cat in self.categories:
            self.processar_categoria(cat)
        logging.info("Pipeline de ingestão raw finalizado.")
