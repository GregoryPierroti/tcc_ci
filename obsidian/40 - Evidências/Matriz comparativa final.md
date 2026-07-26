# Matriz comparativa final

Esta é a síntese comparativa da rodada controlada. A unidade é uma execução
registrada no [[../../results/resultados.csv|arquivo CSV de resultados]]; a duração representa o tempo
total do workflow até aprovação ou primeira falha, e não o tempo isolado de um
check.

## Síntese por tecnologia

| Tecnologia | Execuções | Detectadas | Falsos negativos | Taxa de detecção | Duração média do workflow | Adaptação observada |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Python | 5 | 5 | 0 | 100% | 18,0 s | direta: Ruff, pytest, cobertura e auditoria; fixtures e Docker locais. |
| PySpark | 5 | 3 | 2 | 60% | 54,0 s | complementar: runtime Spark/Java/JDBC e oráculos integrais fora da CI basal. |
| dbt | 5 | 5 | 0 | 100% | 69,2 s | configurada: SQLFluff com templater dbt, adapter PostgreSQL, seeds e testes de dados. |
| **Total** | **15** | **13** | **2** | **86,7%** | **47,1 s** | — |

Taxa de detecção = falhas detectadas pela esteira ÷ falhas introduzidas. Os
dois casos PySpark aprovados pela CI e revelados depois pelo oráculo integral
são classificados como falsos negativos; por isso entram no denominador, mas
não nas detecções.

## Matriz de execuções

| ID | Tecnologia | Classe de falha | Primeiro detector observado | Etapa | Duração | Resultado |
| --- | --- | --- | --- | --- | ---: | --- |
| PY-001 | Python | sintaxe | Ruff format | formatação | 22 s | detectada |
| PY-002 | Python | transformação | pytest | testes determinísticos | 20 s | detectada |
| PY-003 | Python | filtro de join | pytest | testes determinísticos | 18 s | detectada |
| PY-004 | Python | coluna inexistente | pytest | testes determinísticos | 22 s | detectada |
| PY-005 | Python | lockfile inválido | uv | preparação/formatação | 8 s | detectada |
| SP-001 | PySpark | normalização | pytest | testes Spark | 73 s | detectada |
| SP-002 | PySpark | coluna inexistente | pytest | testes Spark | 62 s | detectada |
| SP-003 | PySpark | schema de CNPJ | nenhum na CI basal | oráculo integral externo | 49 s | falso negativo |
| SP-004 | PySpark | tipo de join | nenhum na CI basal | oráculo integral externo | 55 s | falso negativo |
| SP-005 | PySpark | lockfile inválido | uv | preparação/formatação | 31 s | detectada |
| DBT-001 | dbt | SQL inválido | SQLFluff | lint SQL | 57 s | detectada |
| DBT-002 | dbt | referência inexistente | SQLFluff/templater dbt | lint SQL | 67 s | detectada |
| DBT-003 | dbt | CNPJ nulo | teste `not_null` | build/test | 73 s | detectada |
| DBT-004 | dbt | chave duplicada | teste `unique` | build/test | 67 s | detectada |
| DBT-005 | dbt | join semântico | `baseline_counts` | build/test | 82 s | detectada |

## Leitura correta da comparação

- As durações são comparáveis como custo observado do workflow neste ambiente,
  mas não como benchmark universal: cada objeto tem runtime e inicialização
  próprios.
- A taxa de 100% de Python e dbt vale somente para as cinco mutações do
  catálogo de cada objeto. Ela não demonstra cobertura completa do domínio.
- O resultado de PySpark não significa que a tecnologia seja inferior; ele
  mostra que a esteira basal, sem oráculos de cardinalidade e de chaves, não
  detectou as duas mutações semânticas selecionadas.

**Rastreabilidade:** [[Resultados e métricas|resumo numérico dos resultados]],
[[Interpretação comparativa|discussão comparativa]], [[Rastreabilidade das evidências|guia de rastreabilidade]],
[[../../fault-catalog/falhas.yml|catálogo YAML das falhas]] e
[[../../results/resultados.csv|dados canônicos em CSV]].
