# Mapa de tecnologias e checks

## Rodada v1 — evidência histórica

| Tecnologia | Runtime | Esteira | Validação basal | Estado experimental |
| --- | --- | --- | --- | --- |
| Python | Python 3.11, PostgreSQL 16, MinIO | Ruff → pytest/cobertura → pip-audit | 11 delivery / 3 CNPJs | rodada concluída |
| PySpark | Python 3.11, Java 17, PySpark 3.5.2, PostgreSQL 16 | Ruff → testes Spark → pip-audit | 154 linhas / 38 CNPJs | rodada concluída |
| dbt | Python 3.11, dbt 1.9, PostgreSQL 16 | SQLFluff → parse → compile → build/test | 1 linha delivery | rodada concluída |

## Rodada v2 — esteira planejada

| Tecnologia | Checks previstos | Testes previstos | Limite de escopo |
| --- | --- | --- | --- |
| Python | Ruff expandido, mypy, formatador de docstrings, Radon, Vulture, Bandit, pip-audit e Gitleaks | unitários, propriedades, contrato, bootstrap, integração e reexecução | sem métricas de *data quality* |
| PySpark | Ruff expandido, mypy no código de orquestração, formatador de docstrings, Radon, Bandit, pip-audit e Gitleaks | unitários Spark, contrato, bootstrap, integração e reexecução | sem métricas de *data quality* |
| dbt | SQLFluff, parse, compile e controles transversais aplicáveis | integração técnica do projeto dbt | não ampliar testes declarativos de conteúdo na v2 |

Actionlint, Hadolint, cobertura com artefatos, SBOM, pre-commit e proteção de
branch são controles transversais. Esta seção só será atualizada para concluída
após a validação da baseline v2.

## Interpretação por tecnologia

- **Python:** detecções de sintaxe, transformação, join e lockfile; o
  formatador também pode ser primeiro detector.
- **PySpark:** detecta normalização e coluna ausente; não protege, por si só,
  integridade de chaves e cardinalidade da execução integral.
- **dbt:** valida SQL, grafo e testes de dados; detectou as cinco mutações
  selecionadas, inclusive nulidade, duplicidade e cardinalidade.

## Operação

Os READMEs dos objetos são as instruções executáveis:
[[../../projects/02_etl_python/README|guia de execução do ETL Python]],
[[../../projects/03_etl_pyspark/README|guia de execução do ETL PySpark]] e
[[../../projects/04_etl_dbt/README|guia de execução do projeto dbt]].

Para evidência detalhada: [[Fluxo de checks Python|fluxo de checks do Python]],
[[Fluxo de checks PySpark|fluxo de checks do PySpark]] e [[Fluxo de checks dbt|fluxo de checks do dbt]].
Para a síntese transversal: [[../40 - Evidências/Matriz comparativa final|matriz da v1]] e
[[../10 - Especificação/Plano da rodada v2|plano da v2]].
