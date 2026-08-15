# Plano da rodada v2

## Objetivo

Ampliar a esteira de CI com práticas de engenharia de software aplicadas aos
objetos ETL Python, ETL PySpark e dbt/SQL. A v2 mede a capacidade dos checks
de detectar falhas controladas em código, configuração, infraestrutura e
integração técnica.

O escopo exclui *data quality*. Não serão introduzidas métricas ou falhas para
completude, nulidade, unicidade ou cardinalidade do conteúdo dos dados. Quando
um teste inspecionar arquivo, tabela ou schema, ele o fará como contrato técnico
entre componentes, não como juízo sobre qualidade da saída.

## Preservação da v1

`baseline-ci-v1`, `fault-catalog/falhas.yml` e as 15 linhas atuais de
`results/resultados.csv` são evidências históricas imutáveis. A v2 só começa
depois de todos os checks previstos estarem saudáveis, quando será criada a tag
`baseline-ci-v2` e um catálogo próprio.

## Esteira prevista

| Eixo | Técnica ou ferramenta | Papel na v2 |
| --- | --- | --- |
| Formatação e lint | Ruff expandido | Detectar erros, padrões propensos a defeito e problemas de manutenção. |
| Tipagem | mypy | Verificar contratos estáticos de funções e orquestração Python. |
| Documentação | pydocstringformatter | Padronizar docstrings de entradas, saídas, efeitos e exceções. |
| Complexidade | Radon | Sinalizar funções com muitos caminhos independentes. |
| Código morto e arquitetura | Vulture e import-linter | Detectar código abandonado e dependências indevidas entre camadas. |
| Segurança | Bandit, pip-audit e Gitleaks | Analisar código, dependências e segredos versionados. |
| Infraestrutura da CI | Actionlint e Hadolint | Validar workflows e imagens que executam os pipelines. |
| Testabilidade | pytest-cov com mínimo de 95% e relatórios JUnit/XML | Impedir perda de exercitação e registrar evidências. |
| Testes | pytest, Hypothesis e Docker Compose | Separar unidade, propriedade, contrato, bootstrap, integração e reexecução. |
| Governança | pre-commit, SBOM e proteção de branch | Reforçar reprodutibilidade e processo; não são detectores do catálogo. |

Mypy não será usado para alegar validação estática de schemas dinâmicos de
pandas ou Spark. Em PySpark, ele se aplica ao código Python tipável nas
fronteiras de orquestração. Radon é uma métrica de manutenibilidade e
testabilidade, não um teste executável nem prova de correção.

## Hipóteses e dimensão do catálogo

A v2 terá alvo de 28 novas mutações, totalizando 43 execuções quando somadas
às 15 da v1. O catálogo final deve cobrir os eixos abaixo, sem criar mutações
artificiais para controles operacionais que não são detectores.

| Eixo experimental | Mutações v2 planejadas |
| --- | ---: |
| Ruff expandido, mypy, docstrings, complexidade, código morto e arquitetura | 10 |
| Cobertura e testes unitários | 6 |
| Contrato, bootstrap, integração e reexecução | 8 |
| Bandit, Gitleaks, Actionlint e Hadolint | 4 |
| **Total** | **28** |

SBOM, pre-commit, artefatos JUnit/cobertura e proteção de branch entram na
esteira como controles operacionais e evidências, mas não exigem mutação própria.

## Protocolo e evidências

Cada entrada do catálogo v2 deverá conter identificador, arquivo-alvo,
mutação, técnica, princípio de engenharia, detector e etapa esperados,
confirmação técnica independente e limite de interpretação. As execuções usarão
branches isoladas da `baseline-ci-v2`; código defeituoso não entra no `main`.

O CSV continuará sendo a fonte canônica do observado e usará `baseline_tag`
para separar rodadas. A matriz e a interpretação v1 não serão alteradas para
acomodar resultados v2; uma síntese transversal será criada após o encerramento
da nova rodada.

## Critérios para iniciar a v2

1. Documentação de escopo, protocolo e governança atualizada.
2. Checks previstos implementados e disponíveis por comandos locais
   reproduzíveis.
3. Testes unitários e de integração separados.
4. Cobertura configurada com piso de 95% no escopo declarado.
5. Workflow remoto saudável para cada objeto aplicável.
6. Tag `baseline-ci-v2` criada e catálogo v2 revisado antes da primeira
   mutação.

**Relações:** [[Visão e problema de pesquisa|problema de pesquisa]],
[[Desenho metodológico|desenho metodológico]],
[[../20 - Execução/Protocolo de falhas controladas|protocolo]],
[[../20 - Execução/Estado e próximos passos|estado]] e
[[../40 - Evidências/Resultados e métricas|resultados v1]].
