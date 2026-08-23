# Matriz comparativa v1–v2

Esta matriz consolida controles de integração contínua aplicados a pipelines
como práticas de engenharia de software. A evidência primária é uma execução
do [[../../results/resultados.csv|CSV de resultados]]; `execution_id` identifica
a linha, cujo `evidence_url` conduz ao job ou à PR. O catálogo preserva o
detector esperado e o CSV, o primeiro detector observado. A leitura das
categorias segue o [[../10 - Especificação/Desenho metodológico|desenho
metodológico]] e a [[Rastreabilidade das evidências|nota de rastreabilidade]].

## Enquadramento da comparação

| Rodada | Execuções | Mutações únicas | Detecções em execuções | Falsos negativos em execuções | Falsos positivos externos em execuções | Repetições metodológicas |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| v1 | 15 | 15 | 13 | 2 | 0 | 0 |
| v2 | 33 | 28 | 25 | 6 | 2 | 5 |

As quantidades são contagens de linhas do CSV, exceto a coluna de mutações
únicas. A v2 repete V2-PY-003, V2-PY-014, V2-SP-005, V2-SP-007 e V2-GOV-002
para isolar a hipótese ou remover confundidor; não se trata de novas mutações.
Assim, os resultados não autorizam uma comparação direta de “taxa de cobertura”
entre rodadas: os catálogos, os controles e as unidades de análise são
distintos. A referência comparável final da v2 é
`baseline-ci-v2-security-rebuilt-all-20260822` (`14efe37`), mas cada evidência
abaixo preserva o `baseline_tag` da respectiva linha do CSV.

## Evidências v1 preservadas como referência histórica

| Técnica e ferramenta | Risco técnico controlado | Detector esperado → observado | Evidência no CSV | Limite de interpretação | Resultado |
| --- | --- | --- | --- | --- | --- |
| Formatação e análise estática Python (Ruff) | erro de sintaxe no código versionado | Ruff → Ruff format | `2026-07-26-PY-001-01` | O formatador bloqueou antes do lint; não demonstra comportamento funcional. | detecção causal precedente |
| Testes determinísticos Python (pytest) | regressão em transformação ou interface de código | pytest → pytest | `2026-07-26-PY-002-01`, `2026-07-26-PY-003-01`, `2026-07-26-PY-004-01` | Evidência restrita aos cenários do catálogo. | 3 detecções causais |
| Resolução reprodutível de dependências (uv) | lockfile inconsistente | validação do lockfile pelo uv → uv | `2026-07-26-PY-005-01` | Falha de resolução não avalia execução posterior do pipeline. | detecção causal |
| Testes Spark determinísticos (pytest) | regressão de código executado com Spark | pytest → pytest | `2026-07-26-SP-001-01`, `2026-07-26-SP-002-01` | Exercita os casos definidos, não todas as combinações de runtime. | 2 detecções causais |
| Resolução reprodutível PySpark (uv) | lockfile inconsistente | validação do lockfile pelo uv → uv | `2026-07-26-SP-005-01` | Mesmo limite de resolução de dependências. | detecção causal |
| Confirmação integral externa do catálogo histórico | hipóteses que a CI basal não bloqueou | validação externa → nenhum na CI basal | `2026-07-26-SP-003-01`, `2026-07-26-SP-004-01` | Casos históricos fora do eixo de engenharia de software adotado na v2; são preservados como falsos negativos da v1. | 2 falsos negativos |
| Lint SQL e análise do grafo dbt (SQLFluff/templater) | estilo SQL e referência de modelo | dbt parse → SQLFluff / SQLFluff com templater dbt | `2026-07-26-DBT-001-01`, `2026-07-26-DBT-002-02` | O primeiro bloqueio foi precedente ao parse esperado. Em DBT-001, a vírgula removida formou alias implícito e o lint reportou AL02; parse e compile aprovaram. | 2 detecções causais precedentes |
| Checks declarativos do catálogo dbt histórico | verificações declaradas somente na v1 | checks declarativos → checks declarativos | `2026-07-26-DBT-003-03`, `2026-07-26-DBT-004-01`, `2026-07-26-DBT-005-01` | Esses critérios históricos não são transpostos para o escopo técnico da v2 e não sustentam comparação de eficácia entre rodadas. | 3 detecções causais |

## Evidências v2 por técnica

| Técnica e ferramenta | Risco técnico controlado | Detector esperado → observado | Evidência no CSV | Limite de interpretação | Resultado |
| --- | --- | --- | --- | --- | --- |
| Formatação Python (Ruff format) | divergência mecânica em código versionado | Ruff format → Ruff format | `2026-08-16-V2-PY-001-01` | Formatação não prova correção funcional. | detecção causal |
| Lint Python (Ruff F821) | referência a nome inexistente | Ruff F821 → Ruff F821 | `2026-08-16-V2-PY-002-01` | Não cobre resolução exclusivamente dinâmica. | detecção causal |
| Tipagem (mypy) | incompatibilidade entre orquestração e adaptador | mypy → Ruff F401; mypy na repetição | `2026-08-16-V2-PY-003-01`, `2026-08-16-V2-PY-003-02` | A primeira execução foi precedente por import ocioso; a segunda isolou a hipótese de tipos. | precedente e, na repetição, detecção causal |
| Docstrings (pydocstringformatter) | documentação mecanicamente inconsistente | pydocstringformatter → pydocstringformatter | `2026-08-16-V2-PY-004-01` | Formato não garante que a documentação seja verdadeira. | detecção causal |
| Complexidade ciclomática (Radon) | aumento de caminhos independentes | Radon → relatório C (14), sem bloqueio | `2026-08-16-V2-PY-005-01` | `radon cc . -n B -s` reporta o limiar, mas não falha o job. | falso negativo |
| Código morto (Vulture) | caminho privado sem referência | Vulture → escore local de confiança 60/100, CI aprova | `2026-08-16-V2-PY-006-01` | A CI usa `--min-confidence 100`; a mutação não alcançou esse limiar. | falso negativo |
| Arquitetura (import-linter) | dependência invertida entre adaptador e pipeline | import-linter → import-linter | `2026-08-16-V2-PY-007-01` | Cobre somente fronteiras declaradas. | detecção causal |
| Teste unitário Python (pytest) | regressão determinística de normalização | pytest → pytest | `2026-08-16-V2-PY-008-01` | Casos unitários não representam todas as entradas de produção. | detecção causal |
| Teste de propriedade Python (Hypothesis) | violação de invariante de string | pytest com Hypothesis → pytest com Hypothesis | `2026-08-16-V2-PY-009-01` | Entradas geradas não são perfil de produção. | detecção causal |
| Gate de cobertura Python (pytest-cov) | ramo sem exercitação abaixo de 95% das linhas instrumentadas | pytest-cov → cobertura agregada, sem bloqueio | `2026-08-16-V2-PY-010-01` | A composição remota agregou testes e elevou a cobertura; o piso unitário isolado não foi preservado. | falso negativo |
| Integração Python–PostgreSQL (pytest) | contrato de publicação técnica | pytest → pytest | `2026-08-16-V2-PY-011-01` | Não avalia conteúdo analítico. | detecção causal |
| Integração Python–armazenamento de objetos (pytest) | contrato cliente–bucket | pytest → pytest | `2026-08-16-V2-PY-012-01` | Presença de objeto não valida seu conteúdo. | detecção causal |
| Bootstrap Docker Compose (pytest) | infraestrutura de integração incompleta | pytest → pytest | `2026-08-22-V2-PY-013-01` | Não mede política de produção. | detecção causal |
| Reexecução Python (pytest) | ausência de idempotência técnica | pytest → pip-audit `PYSEC-2026-3721`; nenhum na repetição | `2026-08-22-V2-PY-014-01`, `2026-08-22-V2-PY-014-02` | A primeira falha foi `PYSEC-2026-3721` em `pip 26.1.2`, real mas independente da mutação; a repetição mostrou que a suíte não exercita a segunda inicialização. | falso positivo externo e falso negativo |
| Lint PySpark (Ruff F821) | referência a nome inexistente antes do runtime | Ruff F821 → Ruff F821 | `2026-08-22-V2-SP-001-01` | Não valida schema Spark dinâmico. | detecção causal |
| Tipagem PySpark (mypy) | valor incompatível em fronteira tipável | mypy → mypy | `2026-08-22-V2-SP-002-01` | Não infere colunas Spark. | detecção causal |
| Teste unitário Spark (pytest) | regressão de normalização em sessão isolada | pytest → pytest | `2026-08-22-V2-SP-003-01` | Não mede semântica de origem. | detecção causal |
| Teste de propriedade Spark (Hypothesis) | invariante de string em entradas variadas | pytest com Hypothesis → pytest | `2026-08-22-V2-SP-004-01` | A suíte detectou causalmente, mas o teste determinístico também cobre a mutação; não há atribuição exclusiva ao Hypothesis. | detecção causal pela suíte |
| Gate de cobertura PySpark (pytest-cov) | exercitação da orquestração abaixo de 95% das linhas instrumentadas | pytest-cov → pip-audit `PYSEC-2026-3721`; cobertura agregada, sem bloqueio na repetição | `2026-08-22-V2-SP-005-01`, `2026-08-22-V2-SP-005-02` | A primeira falha foi a mesma causa externa `PYSEC-2026-3721`; na repetição, a cobertura de 94,58% das linhas instrumentadas não bloqueou após agregação remota. | falso positivo externo e falso negativo |
| Integração Spark–JDBC (pytest) | indisponibilidade do adaptador | pytest → pytest | `2026-08-22-V2-SP-006-01` | Falha de rede não é falha de conteúdo. | detecção causal |
| Contrato Spark–JDBC (pytest) | divergência entre escrita e leitura técnica | pytest → Ruff format; pytest na repetição | `2026-08-22-V2-SP-007-01`, `2026-08-22-V2-SP-007-02` | A primeira execução foi precedente por formatação; a repetição isolou o contrato JDBC. | precedente e, na repetição, detecção causal |
| Persistência Spark–JDBC (pytest) | ausência de publicação técnica | pytest de integração → pytest unitário de orquestração | `2026-08-22-V2-SP-008-01` | O teste unitário antecedeu a integração prevista; não demonstra propriedades além do contrato de publicação. | detecção causal precedente |
| Lint SQL (SQLFluff) | padrão SQL proibido sem mudança semântica | SQLFluff → SQLFluff LT01 | `2026-08-22-V2-DBT-001-01` | Estilo não prova lógica SQL. | detecção causal |
| Grafo dbt (dbt parse) | referência ausente entre modelos | dbt parse → SQLFluff com templater dbt | `2026-08-22-V2-DBT-002-01` | O lint com templater detectou a mesma causa antes do parse esperado. | detecção causal precedente |
| Segurança de código (Bandit) | execução insegura por `shell=True` | Bandit B602 → Bandit B602 | `2026-08-22-V2-GOV-001-01` | Heurística não prova ausência de vulnerabilidades. | detecção causal direta |
| Segredos versionados (Gitleaks) | assinatura sintética de token | Gitleaks → Bandit B105; nenhum na repetição | `2026-08-22-V2-GOV-002-01`, `2026-08-22-V2-GOV-002-02` | Bandit antecipou a primeira tentativa; em comentário, a assinatura não foi detectada pelo Gitleaks. | precedente e, na repetição, falso negativo |
| Configuração de workflow (Actionlint) | expressão Actions inválida | Actionlint → Actionlint | `2026-08-23-V2-GOV-003-01` | Sintaxe válida não garante política adequada. | detecção causal |
| Higiene de Dockerfile (Hadolint) | camadas de imagem não reprodutíveis | Hadolint → Hadolint DL3009 | `2026-08-23-V2-GOV-004-01` | Lint não substitui scanner de imagem ou teste em runtime. | detecção causal |

## Leitura metodológica

O resultado de uma linha `detected` não basta, por si só, para crédito ao
detector-alvo. As linhas de V2-PY-003, V2-SP-007, V2-SP-008, V2-DBT-002 e
V2-GOV-002 demonstram o papel de controles precedentes. Os uploads posteriores
de JUnit, cobertura ou SBOM sem artefato são efeitos secundários da interrupção
precoce e não aparecem como detectores nesta matriz.

Esta síntese avalia código, dependências, automação, imagem e interfaces
técnicas de pipelines. Não avalia nulidade, completude, unicidade,
cardinalidade ou correção do conteúdo processado; portanto, não sustenta a
alegação de que CI substitui controles de *data quality*.

**Rastreabilidade:** [[Resultados e métricas|resultados e métricas]],
[[Interpretação comparativa|interpretação comparativa]],
[[Rastreabilidade das evidências|guia de rastreabilidade]],
[[../../fault-catalog/falhas.yml|catálogo v1]],
[[../../fault-catalog/falhas-v2.yml|catálogo v2]] e
[[../../results/resultados.csv|dados canônicos em CSV]].
