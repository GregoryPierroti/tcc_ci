# ETL dbt

Este projeto executa o fluxo local `raw → trusted → delivery` com dbt e
PostgreSQL. Os CSVs versionados em `dbt/project/seeds/` são as fontes de
entrada determinísticas; o dbt os carrega no schema `public` e materializa as
camadas `public_trusted` e `public_delivery`.

## Pré-requisitos

- Docker com Docker Compose v2;
- `make` (opcional).

## Execução local

```sh
cp .env.example .env
make run
make status
```

`make run` executa, nessa ordem, `dbt seed --full-refresh` e `dbt build`. A
separação é intencional: os modelos leem fontes declaradas com `source()`, e
os seeds precisam existir antes da construção dos modelos.

## Comandos adicionais

```sh
make debug  # valida imagem, perfil e conexão com o banco local
make parse  # valida a estrutura dbt
make seed   # recarrega somente os dados de exemplo
make build  # materializa e valida os modelos
make test   # executa os oráculos SQL da linha de base
make lint   # valida o SQL com SQLFluff e o templater dbt
make down   # interrompe os serviços preservando o volume local
make reset  # remove somente o volume PostgreSQL deste projeto
```

O ambiente usa Python 3.11, dbt-core/dbt-postgres 1.9.0 e PostgreSQL 16. Não
requer banco externo, credenciais externas ou dados fora do repositório.
