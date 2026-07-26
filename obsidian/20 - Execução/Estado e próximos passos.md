# Estado e próximos passos

> [!important] Ponto de handoff — 2026-07-26
> Antes de retomar experimentos, a próxima sessão deve revalidar a organização
> do vault Obsidian. A organização documental é a prioridade imediata; a rodada
> dbt permanece pausada até essa validação.

## Estado consolidado

| Frente | Situação | Evidência de entrada |
| --- | --- | --- |
| Linha de base e CI | concluídas para Python, PySpark e dbt | [[../10 - Especificação/Linha de base experimental]] |
| Rodada Python | concluída: 5 detecções | [[../40 - Evidências/Resultados e métricas]] |
| Rodada PySpark | concluída: 3 detecções e 2 falsos negativos | [[../40 - Evidências/Resultados e métricas]] |
| Rodada dbt | concluída: 5 detecções | [[Fluxo de checks dbt]] |
| Obsidian | migrado e reorganizado; requer revisão de navegação | [[../00 - Início/00 - Dashboard]] |

## Pendência experimental preservada

As PRs DBT-001 a DBT-005 foram fechadas sem merge após a observação; nenhum
código defeituoso foi integrado ao `main`. Os cinco resultados estão
consolidados no CSV e no [[Fluxo de checks dbt]].

## Revalidação metodológica da rodada dbt

DBT-002 e DBT-003 foram observadas e suas PRs foram encerradas sem merge, mas
não foram consolidadas no CSV. A suspeita de falha basal foi revalidada em
2026-07-26: `make lint` passou localmente no `main` e o workflow manual
**CI - ETL dbt** passou remotamente em todas as etapas. Portanto, não há
correção basal necessária; DBT-002 e DBT-003 devem ser repetidas a partir da
referência saudável antes de DBT-004 e DBT-005.

## Próxima sessão: revalidar o vault

1. Abrir `obsidian/` como vault e iniciar em [[../00 - Início/00 - Dashboard]].
2. Percorrer o fluxo: dashboard → índice mestre → visão/problema → desenho →
   tecnologias → evidências → storytelling.
3. Confirmar que cada assunto tem **uma única nota canônica** e que não há
   conteúdo de especificação fora de `obsidian/`.
4. Verificar se os links para código, catálogo YAML e CSV ajudam a recuperar a
   evidência sem criar uma segunda especificação.
5. Avaliar se os nomes, a granularidade e a ordem servem simultaneamente para
   leitura humana, redação da monografia e contexto de IA.
6. Registrar qualquer ajuste estrutural no [[../50 - Storytelling/Registro metodológico]].

## Após a validação documental

1. Consolidar a matriz final de detecção, duração, adaptação e falsos negativos.
2. Revisar a narrativa comparativa para a monografia.

## Fora de escopo até então

Estas melhorias ficam para depois da rodada dbt e da consolidação comparativa.
Elas não bloqueiam a revisão do vault nem o experimento atual.

| Prioridade | Melhoria | Objetivo | Estado |
| --- | --- | --- | --- |
| 1 | Oráculos integrais de dados na CI | Detectar regressões de cardinalidade e integridade de chaves, como SP-003 e SP-004, que testes unitários não capturaram. | recomendada antes de considerar a esteira suficiente para joins e schemas |
| 2 | Testes nativos dbt | Acrescentar testes unitários/semânticos para ampliar a cobertura das transformações dbt. | a avaliar após DBT-001 a DBT-005 |
| 3 | Auditoria de dependências dbt | Verificar vulnerabilidades nas dependências Python usadas pelo projeto dbt. | não implementada |
| 4 | Mypy | Adicionar análise estática de tipos aos objetos Python e PySpark. | não implementado |
| 5 | Artefatos de cobertura e JUnit | Publicar cobertura e resultados estruturados dos testes na CI para rastreabilidade e visualização. | não implementados; não alteram a capacidade de detecção por si só |
