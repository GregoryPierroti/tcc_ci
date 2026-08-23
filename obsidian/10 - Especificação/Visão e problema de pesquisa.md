# Visão e problema de pesquisa

## O que é avaliado

O TCC avalia a reutilização de uma esteira convencional de integração contínua
em três objetos de engenharia de dados: ETL Python, ETL PySpark e ETL dbt/SQL.
A unidade de análise é a capacidade de cada combinação de checks detectar
falhas controladas, e não a qualidade absoluta dos sistemas.

A rodada v2 delimita a avaliação a práticas de engenharia de software
aplicadas a pipelines: análise estática, documentação de código, segurança,
testabilidade, integração técnica e reprodutibilidade. Ela não avalia *data
quality*; completude, nulidade, unicidade e cardinalidade do conteúdo não são
métricas nem objetivo da rodada.

## Pergunta de pesquisa

Uma esteira de CI usual em software pode ser reutilizada em engenharia de
dados? Quais adaptações são necessárias, quais falhas ela detecta e qual custo
operacional acrescenta?

Na v2, a questão é operacionalizada como: quais práticas de engenharia de
software detectam defeitos de código, configuração, infraestrutura e integração
técnica em pipelines, e quais limites permanecem após sua adoção?

## Resultado esperado

Uma matriz por tecnologia relacionando checks aplicáveis, falhas detectadas,
falsos negativos, duração, estabilidade e nível de adaptação. O diagrama em
[[../00 - Início/diagrama-experimento-ci.jpeg|diagrama do experimento]] é a representação visual desse
desenho.

Veja a [[Especificação do experimento|especificação consolidada]] para critérios e o [[Desenho metodológico|desenho metodológico]]
para o procedimento.

A [[Plano da rodada v2|rodada v2]] preserva a v1 como evidência histórica e
define a ampliação planejada antes de qualquer nova execução.
