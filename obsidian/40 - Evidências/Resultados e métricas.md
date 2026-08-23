# Resultados e métricas v1–v2

Os valores desta nota são derivados do
[[../../results/resultados.csv|CSV canônico]]. “Execução” significa uma linha
do CSV; “mutação única”, um `fault_id` do catálogo. Essa distinção é necessária
porque a v2 possui repetições metodológicas e, por isso, nenhum percentual é
apresentado sem seu denominador.

## Resultado consolidado por rodada

| Rodada | Execuções | Mutações únicas | Detectadas / execuções | Falsos negativos / execuções | Falsos positivos externos / execuções | Duração média por execução |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| v1 | 15 | 15 | 13/15 (86,7%) | 2/15 (13,3%) | 0/15 (0,0%) | 47,1 s |
| v2 | 33 | 28 | 25/33 (75,8%) | 6/33 (18,2%) | 2/33 (6,1%) | 55,5 s |

As proporções são descritivas das **execuções** realizadas, não estimativas de
cobertura de defeitos. Tampouco permitem concluir melhora ou piora entre v1 e
v2: a v2 amplia o catálogo com tipagem, arquitetura, segurança, automação,
imagem, cobertura e contratos técnicos, enquanto a v1 é uma referência
histórica de portfólio diferente.

Nos 33 registros v2, as 25 linhas `detected`, as 6 `false_negative` e as 2
`false_positive` somam as 33 execuções. As cinco repetições — V2-PY-003,
V2-PY-014, V2-SP-005, V2-SP-007 e V2-GOV-002 — explicam a diferença para as
28 mutações únicas. Não há uma taxa única por mutação para a v2 nesta nota,
pois uma mesma hipótese pode registrar detecção precedente e, depois,
repetição isolada com falso negativo ou detecção causal.

## Distribuição por objeto técnico

| Rodada | Objeto | Execuções | Mutações únicas | Detectadas / execuções | Falsos negativos / execuções | Falsos positivos externos / execuções | Duração média por execução |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| v1 | Python | 5 | 5 | 5/5 (100,0%) | 0/5 (0,0%) | 0/5 (0,0%) | 18,0 s |
| v1 | PySpark | 5 | 5 | 3/5 (60,0%) | 2/5 (40,0%) | 0/5 (0,0%) | 54,0 s |
| v1 | dbt | 5 | 5 | 5/5 (100,0%) | 0/5 (0,0%) | 0/5 (0,0%) | 69,2 s |
| v2 | Python | 16 | 14 | 11/16 (68,8%) | 4/16 (25,0%) | 1/16 (6,3%) | 45,3 s |
| v2 | PySpark | 10 | 8 | 8/10 (80,0%) | 1/10 (10,0%) | 1/10 (10,0%) | 79,6 s |
| v2 | dbt | 2 | 2 | 2/2 (100,0%) | 0/2 (0,0%) | 0/2 (0,0%) | 52,0 s |
| v2 | Governança | 5 | 4 | 4/5 (80,0%) | 1/5 (20,0%) | 0/5 (0,0%) | 41,4 s |

“Governança” é um objeto técnico adicional da v2, não uma quarta tecnologia
observada na v1. As durações abrangem todo o workflow até aprovação ou primeiro
bloqueio e incluem provisionamento; não são benchmarks de produção nem tempo
isolado da ferramenta.

## Baselines e ocorrências externas da v2

| `baseline_tag` efetivamente registrado | Execuções v2 | Papel na leitura |
| --- | ---: | --- |
| `baseline-ci-v2` | 15 | Referência inicial da rodada. |
| `baseline-ci-v2-security-rebuilt-20260822` | 6 | Reconstrução comparável após a ocorrência externa de segurança. |
| `baseline-ci-v2-security-rebuilt-all-20260822` | 12 | Referência comparável final (`14efe37`). |

Os dois falsos positivos externos são
`2026-08-22-V2-PY-014-01` e `2026-08-22-V2-SP-005-01`. Ambos registram
`pip-audit PYSEC-2026-3721` em `pip 26.1.2`: o achado de segurança era real,
mas independente da mutação controlada. Portanto, essas linhas não são crédito
de detecção ao pytest ou ao pytest-cov, nem significam erro do pip-audit.

## Controles com limite empírico observado na v2

| Controle avaliado | Execução de evidência | Constatação rastreável | Classificação |
| --- | --- | --- | --- |
| Gate de cobertura Python | `2026-08-16-V2-PY-010-01` | 94,66% das linhas instrumentadas no teste unitário local; a composição remota agregou testes e aprovou. | falso negativo |
| Gate de cobertura PySpark | `2026-08-22-V2-SP-005-02` | 94,58% das linhas instrumentadas no teste unitário local; a composição remota agregou testes e aprovou. | falso negativo |
| Radon | `2026-08-16-V2-PY-005-01` | A complexidade C (14) foi reportada sem tornar o job não zero. | falso negativo |
| Vulture | `2026-08-16-V2-PY-006-01` | A função recebeu escore de confiança 60/100 localmente, abaixo do `--min-confidence 100` da CI. | falso negativo |
| Gitleaks | `2026-08-22-V2-GOV-002-02` | A assinatura sintética em comentário não foi bloqueada após isolar o efeito precedente do Bandit. | falso negativo |
| Reexecução | `2026-08-22-V2-PY-014-02` | A segunda inicialização falha na confirmação independente, mas a suíte remota aprova. | falso negativo |

Esses resultados descrevem limites de configuração e composição dos controles
avaliados. Eles não demonstram ausência de outros defeitos nem constituem uma
medida de cobertura geral.

## Controle de consistência e rastreabilidade

1. Os totais desta nota foram reconciliados com os catálogos
   [[../../fault-catalog/falhas.yml|v1]] e
   [[../../fault-catalog/falhas-v2.yml|v2]]: 15 `fault_id` únicos na v1 e 28
   na v2.
2. Cada total de desfecho corresponde a `outcome` no CSV; detector esperado e
   observado são consultados separadamente em `expected_detector` e
   `observed_detector`.
3. A classificação causal, as repetições e as correções de atribuição são
   detalhadas na [[Rastreabilidade das evidências|nota de rastreabilidade]].
4. A análise se limita a engenharia de software aplicada a pipelines. Não
   avalia nulidade, completude, unicidade, cardinalidade ou correção do
   conteúdo, e não afirma que CI substitui *data quality*.

Veja a [[Matriz comparativa final|matriz por técnica e evidência]] e a
[[Interpretação comparativa|interpretação dos limites]].
