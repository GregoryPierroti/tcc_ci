# Mapa de tecnologias e checks

| Tecnologia | Runtime | Esteira | Oráculo basal | Estado experimental |
| --- | --- | --- | --- | --- |
| Python | Python 3.11, PostgreSQL 16, MinIO | Ruff → pytest/cobertura → pip-audit | 11 delivery / 3 CNPJs | rodada concluída |
| PySpark | Python 3.11, Java 17, PySpark 3.5.2, PostgreSQL 16 | Ruff → testes Spark → pip-audit | 154 linhas / 38 CNPJs | rodada concluída |
| dbt | Python 3.11, dbt 1.9, PostgreSQL 16 | SQLFluff → parse → compile → build/test | 1 linha delivery | rodada concluída |

## Interpretação por tecnologia

- **Python:** detecções de sintaxe, transformação, join e lockfile; o
  formatador também pode ser primeiro detector.
- **PySpark:** detecta normalização e coluna ausente; não protege, por si só,
  integridade de chaves e cardinalidade da execução integral.
- **dbt:** valida SQL, grafo e testes de dados; detectou as cinco mutações
  selecionadas, inclusive nulidade, duplicidade e cardinalidade.

## Operação

Os READMEs dos objetos são as instruções executáveis:
[[../../projects/02_etl_python/README|Python]],
[[../../projects/03_etl_pyspark/README|PySpark]] e
[[../../projects/04_etl_dbt/README|dbt]].

Para evidência detalhada: [[Fluxo de checks Python|fluxo Python]],
[[Fluxo de checks PySpark|fluxo PySpark]] e [[Fluxo de checks dbt|fluxo dbt]].
Para a síntese transversal: [[../40 - Evidências/Matriz comparativa final|matriz comparativa]].
