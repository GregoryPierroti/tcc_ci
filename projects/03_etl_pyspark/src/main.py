import logging
import os
import shutil
from pyspark.sql import SparkSession
from pipeline.ingestao_raw_spark import IngestaoRawSpark
from pipeline.transformacoes_trusted_spark import TransformacoesTrustedSpark
from pipeline.agregacoes_delivery_spark import AgregacoesDeliverySpark

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    spark = None
    try:
        logging.info("🚀 Iniciando pipeline completa (RAW -> TRUSTED -> DELIVERY)")

        jdbc_jar = os.getenv("POSTGRES_JDBC_JAR", "/opt/spark/jars/postgresql-42.7.3.jar")
        spark = SparkSession.builder \
            .appName("PipelineCompletaBancos") \
            .master(os.getenv("SPARK_MASTER", "local[2]")) \
            .config("spark.jars", jdbc_jar) \
            .config("spark.ui.enabled", os.getenv("SPARK_UI_ENABLED", "false")) \
            .getOrCreate()

        base_dir = os.getenv("PIPELINE_BASE_PATH", os.path.dirname(os.path.abspath(__file__)))
        camadas_dir = os.path.join(base_dir, "pipeline", "Camadas")
        shutil.rmtree(camadas_dir, ignore_errors=True)
        logging.info("Camadas Parquet anteriores removidas: %s", camadas_dir)

        # Etapa 1: Ingestão para a camada RAW
        raw = IngestaoRawSpark(spark, base_path=base_dir)
        raw.executar()

        # Etapa 2: Transformação para a camada TRUSTED
        trusted = TransformacoesTrustedSpark(spark, base_path=base_dir)
        trusted.executar()
        
        # Etapa 3: Agregação para a camada DELIVERY e ingestão no Postgres
        delivery = AgregacoesDeliverySpark(spark, base_path=base_dir)
        delivery.executar()

    except Exception as e:
        logging.error(f"Ocorreu um erro na execução do pipeline: {e}", exc_info=True)
        raise
    finally:
        if spark:
            spark.stop()
            logging.info("Sessão Spark finalizada.")

if __name__ == "__main__":
    main()
