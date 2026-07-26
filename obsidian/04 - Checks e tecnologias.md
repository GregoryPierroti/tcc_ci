# Checks e tecnologias

| Tecnologia | Fluxo | Papel |
| --- | --- | --- |
| Python | formatação → lint → pytest/cobertura → dependências | transformações e joins |
| PySpark | formatação → lint → testes Spark → dependências | regras Spark; integração é complementar |
| dbt | SQLFluff → parse → compile → build/testes | SQL, grafo e invariantes de dados |

O mesmo check não protege igualmente todas as tecnologias. Em PySpark, por exemplo, a esteira detectou normalização e coluna ausente, mas não cardinalidade de join.

**Leituras:** [[30 - Tecnologias/Fluxo de checks Python|Python]], [[30 - Tecnologias/Fluxo de checks PySpark|PySpark]] e [[../.github/workflows/ci-dbt.yml|workflow dbt]].
