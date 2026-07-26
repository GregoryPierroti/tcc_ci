# Fluxo de checks do ETL dbt

O workflow `CI - ETL dbt` executa, nesta ordem, lint SQL, validação da
estrutura dbt, compilação e construção/testes. Cada etapa é bloqueante; se uma
falhar, as seguintes são ignoradas. O encerramento dos recursos Docker ocorre
mesmo em caso de falha.

| Ordem | Etapa da CI | Comando | O que verifica |
| ---: | --- | --- | --- |
| 1 | Executar lint SQL | `make lint` | SQLFluff com templater dbt, incluindo estilo e sintaxe SQL renderizada. |
| 2 | Validar estrutura do projeto dbt | `make parse` | Grafo, referências e estrutura do projeto dbt. |
| 3 | Compilar modelos dbt | `make compile` | Renderização e compilação dos modelos SQL. |
| 4 | Executar dbt build e testes | `make test` | Recarrega seeds, executa `dbt build` e depois `dbt test`, incluindo os oráculos de dados declarados. |

## Evidência preliminar: DBT-001

| Falha | Detector esperado no catálogo | Primeiro detector observado | Etapa | Duração | Situação |
| --- | --- | --- | --- | ---: | --- |
| DBT-001, SQL inválido | `dbt parse` | SQLFluff | Executar lint SQL | 57 s | detectada |
| DBT-002, ref inexistente | `dbt parse` | SQLFluff/templater dbt | Executar lint SQL | 67 s | detectada |
| DBT-003, CNPJ nulo | teste `not_null` | `not_null_mod_final_cnpj` | Executar dbt build e testes | 73 s | detectada |

A mutação remove uma vírgula no CTE `bancos` de `mod_final.sql`. Na PR
experimental #30, o job falhou no lint; localmente, `dbt parse` e `dbt compile`
passaram. A vírgula removida tornou `segmento` um alias implícito de `cnpj`;
SQLFluff o reportou como `AL02`. Pelo protocolo, uma etapa anterior que detecta
inequivocamente a mesma mutação conta como `detected`; a divergência entre
esperado e observado permanece registrada no CSV.

## Limite de interpretação

O workflow torna visíveis falhas de estilo/sintaxe, do grafo e da compilação,
além de testes de dados durante a construção. A rodada DBT-002 a DBT-005 ainda
não está consolidada; não se deve inferir taxa de detecção nem suficiência dos
testes dbt antes da conclusão da rodada.

**Fontes:** [[../../.github/workflows/ci-dbt.yml|workflow]],
[[../../projects/04_etl_dbt/Makefile|comandos locais]],
[[../40 - Evidências/Catálogo de falhas|catálogo]] e
[[../20 - Execução/Estado e próximos passos|estado da rodada]].
