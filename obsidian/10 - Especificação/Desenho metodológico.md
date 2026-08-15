# Desenho metodológico

1. Preservar a v1 como linha de base e resultado histórico.
2. Configurar, para a v2, checks locais e remotos adequados a cada tecnologia.
3. Validar a esteira saudável e criar uma tag de referência exclusiva da v2.
4. Injetar uma falha conhecida por vez, em branch experimental isolada.
5. Observar o primeiro detector na CI e executar confirmação técnica
   independente quando a CI passar.
6. Registrar resultado, duração, limitações e comparar tecnologias e rodadas.

## Controles de validade

- Cada rodada possui tag, catálogo e resultados próprios. A v1 usa
  `baseline-ci-v1`; a v2 só começa após a criação de `baseline-ci-v2`.
- Código defeituoso nunca é integrado ao `main`.
- Resultado esperado (catálogo) e resultado observado (CSV) são separados.
- Falsos negativos da v2 são confirmados por teste técnico independente de
  integração, contrato, bootstrap ou reexecução, não por *data quality*.
- Cada falha v2 declara a técnica de engenharia avaliada, detector esperado e
  limite interpretativo.

O procedimento executável está no [[../20 - Execução/Protocolo de falhas controladas|protocolo de falhas controladas]].
O escopo está no [[Plano da rodada v2|plano da v2]].
