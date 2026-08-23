# Estado e próximos passos

> [!important] Ponto de handoff — 2026-08-23
> A rodada v2 foi concluída após V2-GOV-004. Há 33 execuções v2 registradas,
> correspondentes às 28 mutações únicas do catálogo: 25 detectadas, 6 falsos negativos e
> 2 falsos positivos externos.
> As evidências v1 permanecem separadas e imutáveis.

## Estado consolidado

| Frente | Situação | Evidência de entrada |
| --- | --- | --- |
| Linha de base e CI | concluídas para Python, PySpark e dbt | [[../10 - Especificação/Linha de base experimental|linha de base experimental]] |
| Rodada Python | concluída: 5 detecções | [[../40 - Evidências/Resultados e métricas|resultados consolidados]] |
| Rodada PySpark | concluída: 3 detecções e 2 falsos negativos | [[../40 - Evidências/Resultados e métricas|resultados consolidados]] |
| Rodada dbt | concluída: 5 detecções | [[../30 - Tecnologias/Fluxo de checks dbt|fluxo de checks do dbt]] |
| Rodada v2 | 28 de 28 mutações únicas concluídas | `results/resultados.csv`, `fault-catalog/falhas-v2.yml` |
| Obsidian | documentação e narrativa da v1 consolidadas | [[../40 - Evidências/Matriz comparativa final|matriz da v1]] |

## Pendência experimental preservada

As PRs DBT-001 a DBT-005 foram fechadas sem merge após a observação; nenhum
código defeituoso foi integrado ao `main`. Os cinco resultados estão
consolidados no CSV e no [[../30 - Tecnologias/Fluxo de checks dbt|fluxo de checks do dbt]].

## Revalidação metodológica da rodada dbt

DBT-002 e DBT-003 foram repetidas a partir da referência saudável após a
revalidação. `make lint` passou localmente no `main` e o workflow manual
**CI - ETL dbt** passou remotamente em todas as etapas; as repetições, DBT-004
e DBT-005 estão consolidadas no CSV. Não houve correção basal a integrar.

## Próximos passos da v2

1. V2-PY-014 foi repetida de forma causal a partir de
   `baseline-ci-v2-security-rebuilt-all-20260822` (`14efe37`): a referência
   reconstrói `baseline-ci-v2` com apenas a atualização para `pip==26.2` e
   preserva todos os checks da v2. A tag anterior
   `baseline-ci-v2-security-20260822`, derivada da `main` simplificada, fica
   preservada apenas como tentativa não comparável e não será usada nas
   medições. O resultado causal é falso negativo de cobertura de reexecução.
2. Consolidar a interpretação dos resultados a partir da baseline
   reconstruída. V2-PY-001 e
   V2-PY-002 foram detectadas por Ruff, V2-PY-003 foi confirmado por mypy na
   repetição isolada e V2-PY-004 por pydocstringformatter. V2-PY-005 expôs
   falso negativo: Radon reportou C (14), mas sua configuração não bloqueia o
   job. V2-PY-006 expôs outro falso negativo: função morta em 60% de confiança
   não alcança o limiar 100 configurado para Vulture. V2-PY-007 foi detectada
   pelo import-linter na fronteira adaptador-orquestração e V2-PY-008 por
   testes unitários de normalização; V2-PY-009 foi detectada por propriedade
   Hypothesis sobre espaços externos. V2-PY-010 expôs falso negativo: a CI
   agrega cobertura de integração e não preserva o piso unitário de 95%.
   V2-PY-011 e V2-PY-012 foram detectadas por testes de integração PostgreSQL
   e MinIO, respectivamente. V2-PY-013 detectou a ausência do bucket após
   bootstrap. V2-PY-014 expôs falso negativo: a suíte de integração não
   exercita a reinicialização da estrutura já existente. V2-SP-001 foi
   detectada por Ruff F821; V2-SP-002 foi detectada por mypy e V2-SP-003 e
   V2-SP-004 por testes unitários Spark. V2-SP-004 não isolou Hypothesis,
   pois o teste determinístico também cobre a mutação. V2-SP-005 expôs falso
   negativo: a CI agrega cobertura de integração e não preserva o piso unitário
   de 95%. V2-SP-006 detectou a indisponibilidade JDBC e V2-SP-007 o contrato
   de escrita-leitura; a primeira tentativa de V2-SP-007 foi bloqueada por
   formatação e a repetição confirmou o detector previsto. V2-SP-008 detectou
   a ausência de persistência pelo teste unitário de orquestração. V2-DBT-001
   foi detectada por SQLFluff; V2-DBT-002 foi antecipada pelo templater
   SQLFluff antes de dbt parse. V2-GOV-001 foi detectada por Bandit. Na
   V2-GOV-002, o Bandit B105 preemptou a primeira tentativa e a repetição
   isolada revelou falsa negativa do Gitleaks para a assinatura sintética em
   comentário. V2-GOV-003 foi detectada pelo Actionlint na expressão inválida
   do workflow e V2-GOV-004 pelo Hadolint (DL3009). O catálogo v2 está
   integralmente executado; todas as PRs experimentais foram fechadas sem merge.
3. Produzir matriz e interpretação comparativas entre v1 e v2, distinguindo
   detecções causais, precedentes, falsas negativas e falsos positivos externos.

## Handoff para aprofundamento analítico

### Ponto de partida e fontes de verdade

- A execução experimental está encerrada. Não criar novas falhas, não reabrir
  PRs e não alterar a baseline para esta rodada; o trabalho seguinte é
  exclusivamente de consolidação, análise e redação.
- O conjunto observacional primário é `results/resultados.csv`; cada linha é
  uma **execução**, e não necessariamente uma mutação distinta. O catálogo e
  a intenção de cada mutação estão em `fault-catalog/falhas-v2.yml`.
- A síntese técnica está no [[../10 - Especificação/Guia conceitual de CI e engenharia de dados|guia
  conceitual de CI e engenharia de dados]]. Ela relaciona cada conceito,
  ferramenta, risco técnico, aplicação em pipelines e limite de interpretação.
- A referência comparável da v2 é a tag
  `baseline-ci-v2-security-rebuilt-all-20260822` no commit `14efe37`. Não usar
  `baseline-ci-v2-security-20260822`: ela deriva de uma `main` simplificada e
  é explicitamente não comparável.
- A documentação consolidada está na branch
  `docs/rename-data-validations`, commit `ed8aff6`. As evidências da v1 são
  históricas e imutáveis; a comparação deve preservá-las, não recalculá-las.

### Como interpretar os números

- O CSV totaliza 33 execuções para 28 mutações únicas: 25 linhas
  `detected`, 6 `false_negative` e 2 `false_positive` externos. Esses totais
  são descritivos da rodada e não estimativas de cobertura geral.
- Repetições e detecções precedentes devem aparecer explicitamente na matriz:
  V2-PY-003, V2-SP-007 e V2-GOV-002 tiveram repetição para isolar a hipótese;
  V2-DBT-002, V2-GOV-001 e a primeira tentativa de V2-GOV-002 foram
  interrompidas por detector causal precedente. Não atribuir a detecção ao
  detector originalmente esperado quando outro detector falhou antes.
- Os dois falsos positivos externos decorrem de vulnerabilidades transitivas
  de `pip` durante auditoria, não de mutações do catálogo. Mantê-los separados
  de eficácia dos checks. Os falsos negativos são achados sobre limites dos
  controles configurados, não prova de ausência de defeitos.
- A análise deve permanecer em engenharia de software aplicada a pipelines:
  estilo, tipagem, documentação, segurança, complexidade, arquitetura,
  testes, cobertura, integração técnica, automação e imagem. Não introduzir
  métricas de nulidade, unicidade, completude ou outra forma de *data quality*.

### Entregáveis recomendados

1. Construir a matriz v1–v2 por mutação e por técnica, contendo detector
   previsto/observado, estágio, classificação, evidência e limitação de
   interpretação.
2. Redigir a análise por princípio de engenharia: explicar qual risco técnico
   cada ferramenta reduz em pipelines e relacionar as falsas negativas às
   decisões de configuração (por exemplo, limiar, cobertura agregada ou regra
   heurística).
3. Separar, na narrativa, evidência causal, evidência precedente, repetição
   metodológica e falha externa. Só então calcular percentuais, sempre
   informando denominador (execuções ou mutações únicas).
4. Atualizar os artefatos de storytelling e de evidências a partir do CSV;
   manter links para PRs fechadas como trilha de auditoria, sem mesclar código
   experimental.
5. Usar o guia conceitual como pauta para justificar por que cada controle de
   CI é uma prática de engenharia de software aplicável a pipelines, sem
   confundir essa justificativa com avaliação de *data quality*.

### Cuidados operacionais na retomada

- As PRs experimentais #76 a #80 estão fechadas sem merge e suas branches
  remotas foram removidas. A baseline permanece íntegra.
- O checkout principal `tcc_ci` contém alteração local pré-existente em
  `projects/02_etl_python/src/utils/s3_client.py` e artefatos não rastreados
  JUnit/SBOM em Python e PySpark. Não removê-los, não adicioná-los a commits e
  não os confundir com resultados versionados; a branch local atual é
  `fault/v2-py-014-retry`.
- Trabalhar na branch de documentação para a redação e registrar cada marco
  em `Registro metodológico.md` e `Estado e próximos passos.md` antes de
  encerrar uma sessão.

## Escopo aprovado para a v2

O foco é engenharia de software aplicada a pipelines, não *data quality*.
Nulidade, unicidade, completude e cardinalidade do conteúdo não serão novos
critérios experimentais. Contrato, bootstrap, integração e reexecução são
avaliados como comportamentos técnicos entre componentes.

| Prioridade | Ampliação | Objetivo | Estado |
| --- | --- | --- | --- |
| 1 | Ruff expandido, mypy, docstrings, Radon e cobertura mínima | Prevenir defeitos estáticos e tornar a testabilidade mensurável. | implementada e validada localmente |
| 2 | Bandit, Gitleaks, Actionlint e Hadolint | Cobrir segurança de código, segredos, workflow e contêiner. | implementada e validada localmente |
| 3 | Testes unitários, contratos e integração separados | Verificar código isolado e integração técnica em ambiente efêmero. | implementada e validada localmente |
| 4 | Bootstrap e reexecução | Verificar criação de recursos e idempotência técnica. | implementada e validada localmente |
| 5 | Artefatos JUnit/cobertura, SBOM e governança de merge | Produzir rastreabilidade e reforçar o processo de CI. | implementada e validada remotamente |
