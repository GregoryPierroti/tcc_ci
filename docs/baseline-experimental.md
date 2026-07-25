# Linha de base experimental

Data de consolidação: 2026-07-25.

Este documento registra o estado local reproduzível dos três objetos
experimentais antes da introdução de CI. Os dados de entrada são pequenos,
versionados e determinísticos, e cada projeto fornece comandos `make` para a
execução local.

| Objeto | Runtime e infraestrutura | Comando de execução | Oráculo mínimo observado |
| --- | --- | --- | --- |
| `02_etl_python` | Python 3.11, PostgreSQL 16 e MinIO | `make run` | `raw/trusted`: bancos 1474, reclamações 918, empregados 39; `delivery.bancos_unificados`: 11 linhas e 3 CNPJs distintos |
| `03_etl_pyspark` | Python 3.11, Java 17, PySpark 3.5.0 e PostgreSQL 16 | `make run` | `reclamacoes_consolidadas`: 154 linhas e 38 CNPJs distintos |
| `04_etl_dbt` | Python 3.11, dbt-core/dbt-postgres 1.9.0 e PostgreSQL 16 | `make run` | trusted: bancos 1474, reclamações 918, empregados 39; `public_delivery.mod_final`: 1 linha |

## Convenções comuns

- Cada projeto possui `README.md`, `.env.example`, `docker-compose.yaml` e
  `Makefile`.
- `make reset` remove apenas os volumes Docker locais do respectivo projeto;
  os dados versionados não são removidos.
- `make down` encerra os serviços preservando o volume local.
- As verificações locais serão expostas por `make test`. Elas não são uma
  esteira de CI e não executam automaticamente no GitHub nesta fase.
- Os checks de qualidade locais são expostos por `make format-check` e
  `make lint`; nos projetos Python, `make security` executa a auditoria de
  dependências. Esses comandos serão a interface chamada pela CI posterior.

## Interpretação comparativa

As contagens delivery não devem ser usadas como critério de equivalência entre
os três objetos. Os projetos preservam regras de junção distintas, herdadas da
fonte: pandas usa junções internas, PySpark usa junção final à esquerda e dbt
usa um conjunto menor de correspondências. Nesta fase, a comparação mede a
capacidade de verificações de software em tecnologias diferentes; não altera a
regra de negócio para tornar os resultados artificialmente iguais.

## Critérios da linha de base

Uma versão basal é aceita quando:

1. `docker compose config` é válido;
2. a execução descrita no README termina sem erro em banco local vazio;
3. os oráculos mínimos da tabela acima são observados;
4. a reexecução não falha e preserva a saída esperada;
5. os testes locais determinísticos passam.
6. os checks locais de formatação, lint e dependências aplicáveis passam.
