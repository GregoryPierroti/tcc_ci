# Estado e próximos passos

> [!important] Ponto de handoff — 2026-07-26
> As três rodadas estão concluídas e a análise comparativa foi consolidada. O
> próximo trabalho é executar a v2 de engenharia de software, mantendo as
> evidências v1 separadas dos novos resultados.

## Estado consolidado

| Frente | Situação | Evidência de entrada |
| --- | --- | --- |
| Linha de base e CI | concluídas para Python, PySpark e dbt | [[../10 - Especificação/Linha de base experimental|linha de base experimental]] |
| Rodada Python | concluída: 5 detecções | [[../40 - Evidências/Resultados e métricas|resultados consolidados]] |
| Rodada PySpark | concluída: 3 detecções e 2 falsos negativos | [[../40 - Evidências/Resultados e métricas|resultados consolidados]] |
| Rodada dbt | concluída: 5 detecções | [[../30 - Tecnologias/Fluxo de checks dbt|fluxo de checks do dbt]] |
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

1. Executar as 20 mutações restantes de forma isolada a partir da tag
   `baseline-ci-v2` e consolidar os resultados observados; V2-PY-001 e
   V2-PY-002 foram detectadas por Ruff, V2-PY-003 foi confirmado por mypy na
   repetição isolada e V2-PY-004 por pydocstringformatter. V2-PY-005 expôs
   falso negativo: Radon reportou C (14), mas sua configuração não bloqueia o
   job. V2-PY-006 expôs outro falso negativo: função morta em 60% de confiança
   não alcança o limiar 100 configurado para Vulture. V2-PY-007 foi detectada
   pelo import-linter na fronteira adaptador-orquestração e V2-PY-008 por
   testes unitários de normalização.
2. Ao final, produzir matriz e interpretação comparativas entre v1 e v2.

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
