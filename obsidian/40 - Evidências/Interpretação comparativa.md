# Interpretação comparativa

## Resposta à pergunta orientadora

A esteira convencional de CI foi reutilizável nos três objetos, mas não de
forma idêntica. Python recebeu checks diretamente familiares ao ecossistema de
software; PySpark exigiu runtime e testes Spark e revelou a necessidade de
oráculos integrais; dbt exigiu lint consciente de templates, compilação do
grafo e testes de dados. Portanto, a reutilização é viável quando os checks
genéricos são combinados com verificações específicas da transformação e dos
dados.

## O que os resultados sustentam

1. Checks antecipados são úteis: Ruff, `uv` e SQLFluff impediram falhas antes
   das etapas de testes previstas em alguns casos.
2. Testes de unidade/determinísticos detectaram mudanças de transformação,
   normalização, filtro e referência inválida nos objetos Python e PySpark.
3. Os testes declarativos dbt detectaram nulidade, duplicidade e cardinalidade
   da saída; a rodada selecionada obteve cinco detecções em cinco mutações.
4. A CI basal de PySpark não assegurou preservação de chaves ou cardinalidade:
   SP-003 gerou delivery vazio e SP-004 elevou-o de 154 para 1.589 linhas sem
   falhar no workflow.

## Limites e ameaças à validade

- O experimento possui cinco mutações por tecnologia, selecionadas e
  controladas. As proporções observadas não são estimativas estatísticas de
  toda a classe de defeitos possível.
- O primeiro detector pode diferir do detector esperado no catálogo. Isso é
  registrado como comportamento da esteira, não como alteração retrospectiva
  da hipótese experimental.
- Duração inclui provisionamento e execução no GitHub Actions; ela descreve
  este ambiente e não substitui medição de desempenho de produção.
- Os oráculos integrais foram usados para confirmar aprovados da CI. Eles são
  essenciais para interpretar falsos negativos, mas ainda não pertencem à
  esteira basal PySpark.

## Implicação prática

Para Python e dbt, a combinação atual forneceu cobertura observada para o
catálogo executado. Para PySpark, o próximo reforço prioritário é trazer para a
CI os oráculos de contagem, cardinalidade e integridade de chaves usados na
execução integral. Cobertura de código, sozinha, não substitui esses oráculos.

Veja a [[Matriz comparativa final|matriz]], o [[Resultados e métricas|resumo
numérico]] e o [[../20 - Execução/Estado e próximos passos|backlog posterior]].
