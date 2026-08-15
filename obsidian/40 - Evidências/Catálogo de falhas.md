# Catálogo de falhas da v1

O [[../../fault-catalog/falhas.yml|catálogo YAML das falhas]] é a evidência estruturada
das mutações: identificador, arquivo-alvo, detector e etapa esperados. Esta
nota define como ele entra na narrativa.

| Tecnologia | Série | Estado |
| --- | --- | --- |
| Python | PY-001 a PY-005 | executada e consolidada |
| PySpark | SP-001 a SP-005 | executada e consolidada |
| dbt | DBT-001 a DBT-005 | executada e consolidada |

O catálogo não é o resultado: a observação canônica está em
[[Resultados e métricas|resumo dos resultados]] e no [[../../results/resultados.csv|arquivo CSV canônico]].

O arquivo atual é imutável como catálogo da v1. A v2 terá catálogo próprio,
criado somente após a baseline `baseline-ci-v2`, com técnica de engenharia,
princípio, detector esperado, confirmação técnica e limitação de cada mutação.
Veja [[../10 - Especificação/Plano da rodada v2|o plano da v2]].
