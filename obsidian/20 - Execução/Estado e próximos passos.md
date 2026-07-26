# Estado e próximos passos

> [!important] Ponto de handoff — 2026-07-26
> As três rodadas estão concluídas e a análise comparativa foi consolidada. O
> próximo trabalho é transformar as evidências em redação de monografia ou
> implementar melhorias futuras de cobertura, sem misturá-las aos resultados
> já medidos.

## Estado consolidado

| Frente | Situação | Evidência de entrada |
| --- | --- | --- |
| Linha de base e CI | concluídas para Python, PySpark e dbt | [[../10 - Especificação/Linha de base experimental|linha de base experimental]] |
| Rodada Python | concluída: 5 detecções | [[../40 - Evidências/Resultados e métricas|resultados consolidados]] |
| Rodada PySpark | concluída: 3 detecções e 2 falsos negativos | [[../40 - Evidências/Resultados e métricas|resultados consolidados]] |
| Rodada dbt | concluída: 5 detecções | [[../30 - Tecnologias/Fluxo de checks dbt|fluxo de checks do dbt]] |
| Obsidian | matriz, interpretação, evidências e narrativa final consolidadas | [[../40 - Evidências/Matriz comparativa final|matriz comparativa final]] |

## Pendência experimental preservada

As PRs DBT-001 a DBT-005 foram fechadas sem merge após a observação; nenhum
código defeituoso foi integrado ao `main`. Os cinco resultados estão
consolidados no CSV e no [[../30 - Tecnologias/Fluxo de checks dbt|fluxo de checks do dbt]].

## Revalidação metodológica da rodada dbt

DBT-002 e DBT-003 foram repetidas a partir da referência saudável após a
revalidação. `make lint` passou localmente no `main` e o workflow manual
**CI - ETL dbt** passou remotamente em todas as etapas; as repetições, DBT-004
e DBT-005 estão consolidadas no CSV. Não houve correção basal a integrar.

## Próximos passos de redação

1. Usar a [[../40 - Evidências/Matriz comparativa final|matriz comparativa final]] como tabela de
   resultados da monografia.
2. Converter a [[../40 - Evidências/Interpretação comparativa|discussão comparativa]]
   em discussão, ameaças à validade e conclusão.
3. Manter a [[../40 - Evidências/Rastreabilidade das evidências|rastreabilidade das evidências]]
   como apêndice ou guia de auditoria.

## Fora de escopo até então

Estas melhorias ficam para depois da rodada dbt e da consolidação comparativa.
Elas não bloqueiam a revisão do vault nem o experimento atual.

| Prioridade | Melhoria | Objetivo | Estado |
| --- | --- | --- | --- |
| 1 | Validações integrais de dados na CI | Detectar regressões de cardinalidade e integridade de chaves, como SP-003 e SP-004, que testes unitários não capturaram. | recomendada antes de considerar a esteira suficiente para joins e schemas |
| 2 | Testes nativos dbt | Acrescentar testes unitários/semânticos para ampliar a cobertura das transformações dbt. | a avaliar após DBT-001 a DBT-005 |
| 3 | Auditoria de dependências dbt | Verificar vulnerabilidades nas dependências Python usadas pelo projeto dbt. | não implementada |
| 4 | Mypy | Adicionar análise estática de tipos aos objetos Python e PySpark. | não implementado |
| 5 | Artefatos de cobertura e JUnit | Publicar cobertura e resultados estruturados dos testes na CI para rastreabilidade e visualização. | não implementados; não alteram a capacidade de detecção por si só |
