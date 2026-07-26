# Próximos passos do experimento

Este documento organiza a sequência de trabalho após a preparação dos três
objetos experimentais e da primeira versão das pipelines GitHub Actions.

O [diagrama do experimento](diagrama-experimento-ci.jpeg) apresenta a visão
geral que orienta esta sequência: checks de CI aplicados aos três objetos,
falhas controladas e coleta de métricas de detecção, duração e adaptação.
Ele é uma referência metodológica; os checks efetivamente disponíveis em cada
objeto são os registrados neste documento e no diário metodológico.

## Estado atual

- ETL Python, ETL PySpark e ETL dbt executam localmente com Docker Compose e
  dados versionados.
- Cada objeto possui pipeline bloqueante no GitHub Actions.
- Python e PySpark executam Ruff, pytest, pytest-cov e pip-audit.
- dbt executa SQLFluff, `dbt parse`, `dbt compile`, `dbt build` e `dbt test`.
- O diário metodológico registra decisões, evidências e limitações em
  `obsidian/50 - Storytelling/Registro metodológico.md`.

## Próxima feature: baseline e catálogo de falhas

Objetivo: definir as falhas controladas antes de modificar qualquer objeto
experimental.

1. Criar uma tag Git do baseline saudável, por exemplo `baseline-ci-v1`.
2. Criar `fault-catalog/falhas.yml` com 5 a 6 falhas iniciais por projeto.
3. Criar o protocolo de falhas controladas com o procedimento repetível de
   injeção, execução, registro e retorno ao baseline.
4. Criar o modelo inicial de `results/resultados.csv`.

Critério de conclusão: uma pessoa deve conseguir escolher uma falha do
catálogo, aplicá-la em uma branch própria, executar a pipeline e registrar o
resultado sem decidir o procedimento durante a execução.

Os artefatos desta feature são `fault-catalog/falhas.yml`,
`results/resultados.csv`. A tag
`baseline-ci-v1` identifica o commit saudável a partir do qual toda execução
de falha deve começar.

## Primeira rodada de falhas

Aplicar uma falha por branch e por pull request. Cada PR deve partir do
baseline e conter somente a mutação listada no catálogo.

Ordem recomendada:

1. Python: sintaxe, regra de transformação, cardinalidade de join e dependência.
2. PySpark: schema, coluna inexistente, cardinalidade de join e agregação.
3. dbt: SQL inválido, `ref` inexistente, violação de `not_null`/`unique` e
   transformação que compila mas produz resultado incorreto.

Para cada execução, registrar projeto, identificador da falha, commit,
detector esperado, etapa que falhou, status observado, duração e classificação
de falso positivo ou falso negativo.

## Coleta e análise

Depois da primeira rodada:

1. Consolidar os resultados no CSV.
2. Calcular taxa de detecção, falhas por etapa, falsos negativos e duração.
3. Comparar os objetos sem tratar cobertura como prova de qualidade.
4. Registrar limitações: diferenças de runtime, dependências, testes
   disponíveis e limitações conhecidas das ferramentas.

## Melhorias posteriores, somente se necessárias

- Publicar `coverage.xml` e relatórios de teste como artefatos do GitHub Actions.
- Adicionar JUnit XML para facilitar a consolidação automática.
- Avaliar `pip-audit` para a imagem dbt.
- Reavaliar mypy após haver mais funções Python com tipos explícitos.
- Avaliar testes unitários nativos do dbt sem substituir os testes de dados
  já adotados.

Esses itens não devem bloquear o início da primeira rodada de falhas.
