# Linha do tempo metodológica

## Ato 1 — Construção de uma base reproduzível

DEC-001 a DEC-009 e ETP-001 a ETP-014 registram a escolha do monorepo, a
recuperação dos três objetos, infraestrutura Docker e consolidação da linha
de base.

## Ato 2 — Qualidade e CI como objeto de estudo

DEC-010 a DEC-016 e ETP-015 a ETP-025 registram as ferramentas locais, as
pipelines, as correções mínimas e a ampliação de verificações.

## Ato 3 — Experimento controlado

ETP-026 e ETP-027 introduzem o diagrama, a tag basal, o catálogo e o protocolo.
ETP-028 a ETP-032 cobrem Python; ETP-033 a ETP-038 cobrem PySpark; ETP-039 a
ETP-043 registram a revisão documental, a revalidação basal e o encerramento
da rodada dbt.

## Tese narrável

A CI convencional foi transferida para os três objetos com adaptações por
tecnologia. Ela encontrou muitas falhas, mas a rodada PySpark demonstra que
checks unitários e de qualidade não substituem oráculos integrais de dados.
Python e dbt detectaram todas as cinco mutações selecionadas; PySpark detectou
três e deixou passar duas falhas semânticas, reveladas somente pelo oráculo
integral. A conclusão comparativa é que a CI é reutilizável, desde que checks
gerais sejam complementados por oráculos específicos de dados.

**Resultados:** [[../40 - Evidências/Matriz comparativa final|matriz final das 15 execuções]] e
[[../40 - Evidências/Interpretação comparativa|discussão comparativa]].
**Diário completo:** [[Registro metodológico|diário metodológico completo]].
