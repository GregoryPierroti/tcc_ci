# Especificação do experimento

## Problema e resultado esperado

Avaliar se práticas de CI de software são aplicáveis a uma stack de engenharia
de dados com Python, PySpark e SQL/dbt. O resultado esperado é uma matriz por
tecnologia que informe checks aplicáveis, falhas detectadas, adaptações e custo
de execução.

## Desenho experimental

| Elemento | Especificação |
| --- | --- |
| Objetos | ETL Python, ETL PySpark e ETL dbt |
| Linha de base | tag `baseline-ci-v1` |
| Entrada | dados pequenos, versionados e determinísticos |
| Execução | Docker Compose e interface `make` |
| CI | GitHub Actions, uma pipeline bloqueante por objeto |
| Tratamento | uma mutação por branch/PR; código defeituoso não entra em `main` |
| Evidência | catálogo YAML, CSV de resultados, diário metodológico e PRs |

## Critérios de baseline

Uma base é aceita se Compose é válido, a execução limpa funciona, o oráculo
mínimo aparece, a reexecução é estável, checks aplicáveis passam e os três
workflows remotos aprovam. Os oráculos e runtimes concretos estão em
[[../../docs/baseline-experimental|Linha de base experimental]].

## Premissas comparativas

As três saídas delivery não precisam ter a mesma cardinalidade, pois preservam
regras herdadas distintas. A comparação mede a capacidade dos checks, não a
equivalência artificial das regras de negócio.

**Fontes:** [[../../docs/diagrama-experimento-ci.jpeg|diagrama]],
[[../../docs/baseline-experimental|baseline]] e
[[../../docs/registro-metodologico|registro]].
