# ETL PySpark

Este projeto executa o fluxo local `RAW → Trusted → Delivery` com PySpark.
Os dados versionados em `src/pipeline/Dados/` são materializados como Parquet
em `src/pipeline/Camadas/` e a saída final é gravada no PostgreSQL local como
`reclamacoes_consolidadas`.

## Pré-requisitos

- Docker com Docker Compose v2;
- `make` (opcional).

## Execução local

```sh
cp .env.example .env
make run
make status
make test
```

O ambiente inclui Java 17, PySpark 3.5, o driver JDBC PostgreSQL e PostgreSQL
16. A sessão usa `local[2]`; não há dependência de cluster nem de download de
driver JDBC durante a execução.

## Reexecução limpa

```sh
make reset
make run
```

`make reset` remove somente o volume PostgreSQL deste projeto. A execução
seguinte sobrescreve os Parquets gerados; os dados de entrada versionados não
são removidos.
