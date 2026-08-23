# Rastreabilidade das evidências

## Fontes canônicas e encadeamento

| Evidência | Papel no experimento | Fonte canônica |
| --- | --- | --- |
| Mutações, técnica, detector e etapa esperados da v1 | Hipótese operacional histórica da primeira rodada. | [[../../fault-catalog/falhas.yml|catálogo YAML v1]] |
| Mutações, técnica, confirmação independente e limite da v2 | Hipótese operacional da rodada de engenharia de software aplicada a pipelines. | [[../../fault-catalog/falhas-v2.yml|catálogo YAML v2]] |
| Resultado observado, baseline, duração e URL do job | Dado primário de cada execução. | [[../../results/resultados.csv|dados brutos em CSV]] |
| PRs e jobs remotos | Reprodução auditável da execução. | Campo `evidence_url` de cada linha do CSV. |
| Decisões, reexecuções, confirmações e exceções | Contexto metodológico e limites de interpretação. | [[../50 - Storytelling/Registro metodológico|diário metodológico]] |
| Workflows e comandos | Implementação da esteira observada. | [[../../.github/workflows|workflows de CI]] e READMEs dos projetos. |

O caminho de auditoria é: **catálogo → linha do CSV → URL do job/PR → diário
metodológico**. O catálogo preserva a expectativa; o CSV preserva o observado;
o job demonstra a execução remota; e o diário explica confirmações técnicas,
baseline e decisões de isolamento. Não se altera a expectativa do catálogo
para fazê-la coincidir com um detector antecipado.

| Elemento de interpretação | Registro e tratamento |
| --- | --- |
| Detector esperado | Hipótese do catálogo (`expected_detector` e `expected_stage`); permanece imutável durante a leitura do resultado. |
| Detector observado | Primeiro bloqueio da linha no CSV (`observed_detector` e `observed_stage`); pode coincidir com o esperado, precedê-lo ou estar ausente. |
| Causa externa | Fato real independente da mutação, identificado em `observed_detector` e nas notas; é excluído da atribuição de eficácia da hipótese. |
| Efeito secundário | Consequência posterior à interrupção, como artefato não produzido para upload; é descrita nas notas, sem crédito de detecção. |

## Rodadas e referências basais

| Rodada ou referência | Papel de leitura |
| --- | --- |
| `baseline-ci-v1` | Linha de base histórica da v1; seus 15 resultados registrados permanecem imutáveis. |
| `baseline-ci-v2` (`e5f65d8`) | Referência inicial da v2. Parte das execuções preserva essa tag no campo `baseline_tag`. |
| `baseline-ci-v2-security-rebuilt-20260822` (`b80ccfa`) | Reconstrução comparável da v2 que atualizou somente `pip==26.2` na referência original. |
| `baseline-ci-v2-security-rebuilt-all-20260822` (`14efe37`) | Referência comparável final, que preserva os checks v2 e incorpora a reconstrução de segurança também para PySpark. |
| `baseline-ci-v2-security-20260822` | Tentativa derivada de uma `main` simplificada; é não comparável e não deve ser usada como referência de medição. |

O CSV conserva o `baseline_tag` efetivamente usado em cada execução. A tag
`baseline-ci-v2-security-rebuilt-all-20260822` é a referência comparável final,
mas não deve substituir retrospectivamente as tags registradas nas 33 linhas da
v2.

## Repetições metodológicas da v2

| `fault_id` | Execuções preservadas no CSV | Motivo e leitura correta |
| --- | --- | --- |
| V2-PY-003 | `2026-08-16-V2-PY-003-01` e `2026-08-16-V2-PY-003-02` | Ruff F401 detectou causalmente um import ocioso antes de mypy; a repetição isolou a incompatibilidade de tipos. |
| V2-PY-014 | `2026-08-22-V2-PY-014-01` e `2026-08-22-V2-PY-014-02` | A primeira execução foi interrompida por vulnerabilidade externa de `pip`; a repetição em baseline reconstruída confirmou o falso negativo de reexecução. |
| V2-SP-005 | `2026-08-22-V2-SP-005-01` e `2026-08-22-V2-SP-005-02` | A primeira execução sofreu a mesma causa externa de `pip`; a repetição isolou o falso negativo do gate de cobertura agregada. |
| V2-SP-007 | `2026-08-22-V2-SP-007-01` e `2026-08-22-V2-SP-007-02` | Ruff format bloqueou primeiro; a repetição formatada isolou o contrato técnico JDBC previsto. |
| V2-GOV-002 | `2026-08-22-V2-GOV-002-01` e `2026-08-22-V2-GOV-002-02` | Bandit B105 detectou causalmente a constante antes de Gitleaks; a assinatura em comentário isolou a hipótese e revelou o falso negativo de Gitleaks. |

Repetição não é nova mutação e não elimina a primeira linha. Por isso, a v2
tem 33 execuções para 28 `fault_id` únicos. Toda proporção deve informar se usa
execuções ou mutações únicas como denominador.

## Regras de atribuição causal

1. **Detecção causal** é o primeiro bloqueio diretamente causado pela mutação.
2. **Detecção causal precedente** ocorre quando outro controle, ou um estágio
   anterior, bloqueia a mesma causa antes do detector esperado. Ela não permite
   atribuir a detecção ao detector-alvo sem uma repetição isolada.
3. **Falso negativo** exige confirmação técnica independente da falha e
   aprovação da CI pelo controle avaliado.
4. **Falso positivo externo** é uma falha do workflow por causa real, porém
   independente da mutação. V2-PY-014-01 e V2-SP-005-01 registram duas
   ocorrências de `PYSEC-2026-3721` em `pip 26.1.2`; não são falsos alertas do
   pip-audit nem detecções das mutações.
5. Uploads JUnit, cobertura ou SBOM que falham após interrupção precoce por
   ausência de artefato são **efeitos secundários**. Não são detectores causais
   nem falsos positivos externos.

| Caso | Atribuição preservada |
| --- | --- |
| V2-GOV-001 | Detecção causal direta por Bandit B602. O detector esperado e o observado coincidem; a diferença de rótulo da etapa não a torna precedente. |
| V2-SP-008 | Detecção causal precedente: o teste unitário de orquestração interceptou a ausência de persistência antes da integração JDBC prevista. |
| V2-SP-004 | Detecção causal na suíte pytest, mas sem atribuição exclusiva ao Hypothesis, pois o teste determinístico também cobre a mutação. |
| DBT-001 da v1 | SQLFluff detectou AL02 porque a vírgula removida tornou `segmento` um alias implícito de `cnpj`; `dbt parse` e `compile` passaram. A evidência não deve ser resumida como “SQL inválido”. |

## Regras de leitura adicionais

1. Cada execução do CSV possui identificador, baseline, commit da mutação,
   duração, desfecho e URL do job. A v1 contém 15 execuções e a v2, 33; os
   totais são descritivos dos catálogos executados, não medidas de cobertura
   geral.
2. Branches e PRs defeituosos foram fechados sem merge; a `main` não contém as
   mutações experimentais.
3. A revalidação basal dbt ocorreu no workflow manual
   [#30215534482](https://github.com/GregoryPierroti/tcc_ci/actions/runs/30215534482),
   aprovado em todas as etapas antes das repetições consolidadas.
4. A análise da v2 permanece restrita a engenharia de software e interfaces
   técnicas de pipelines. Ela não introduz medidas de nulidade, completude,
   unicidade, cardinalidade ou correção do conteúdo dos dados.

Use esta nota para recuperar uma afirmação da futura [[Matriz comparativa final|matriz v1–v2]]
até o registro estruturado e, quando necessário, até o job remoto correspondente.
