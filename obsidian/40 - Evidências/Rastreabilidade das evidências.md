# Rastreabilidade das evidências

| Evidência | Papel no experimento | Fonte canônica |
| --- | --- | --- |
| Mutações e detector/etapa esperados | hipótese operacional de cada falha | [[../../fault-catalog/falhas.yml|falhas.yml]] |
| Resultado observado, duração e URL do job | dado primário de cada execução | [[../../results/resultados.csv|resultados.csv]] |
| PRs e jobs remotos | reprodução auditável da execução | URL `evidence_url` de cada linha do CSV |
| Decisões, reexecuções e exceções | contexto metodológico e limitações | [[../50 - Storytelling/Registro metodológico|registro]] |
| Workflows e comandos | implementação da esteira observada | [[../../.github/workflows|workflows]] e READMEs dos projetos |

## Regras de leitura

1. O catálogo expressa o esperado; o CSV preserva o observado. Não se edita o
   esperado para fazê-lo coincidir com um detector antecipado.
2. Cada execução do CSV tem um identificador, commit da mutação, duração,
   desfecho e URL do job. São 15 execuções, cinco por tecnologia.
3. Branches e PRs defeituosos foram fechados sem merge; a `main` não contém as
   mutações experimentais.
4. A revalidação basal dbt ocorreu no workflow manual
   [#30215534482](https://github.com/GregoryPierroti/tcc_ci/actions/runs/30215534482),
   aprovado em todas as etapas antes das repetições consolidadas.

Use esta nota para recuperar uma afirmação da [[Matriz comparativa final]] até
o registro estruturado e, quando necessário, até o job remoto correspondente.
