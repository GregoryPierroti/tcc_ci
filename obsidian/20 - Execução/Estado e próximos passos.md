# Estado e próximos passos

> [!important] Ponto de handoff — 2026-08-22
> A rodada v2 foi revalidada após V2-SP-005. Há 22 execuções v2 registradas,
> correspondentes a 19 mutações únicas: 15 detectadas, 5 falsos negativos e
> 2 falsos positivos externos.
> As evidências v1 permanecem separadas e imutáveis.

## Estado consolidado

| Frente | Situação | Evidência de entrada |
| --- | --- | --- |
| Linha de base e CI | concluídas para Python, PySpark e dbt | [[../10 - Especificação/Linha de base experimental|linha de base experimental]] |
| Rodada Python | concluída: 5 detecções | [[../40 - Evidências/Resultados e métricas|resultados consolidados]] |
| Rodada PySpark | concluída: 3 detecções e 2 falsos negativos | [[../40 - Evidências/Resultados e métricas|resultados consolidados]] |
| Rodada dbt | concluída: 5 detecções | [[../30 - Tecnologias/Fluxo de checks dbt|fluxo de checks do dbt]] |
| Rodada v2 (parcial) | 19 de 28 mutações únicas concluídas; 9 restantes | `results/resultados.csv`, `fault-catalog/falhas-v2.yml` |
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
2. Executar as 9 mutações restantes de forma isolada a partir da baseline
   reconstruída e
   consolidar os resultados observados; V2-PY-001 e
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
   de 95%. A próxima é V2-SP-006, de integração Spark-JDBC.
3. Ao final, produzir matriz e interpretação comparativas entre v1 e v2.

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
