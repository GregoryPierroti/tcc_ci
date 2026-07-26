# Desenho metodológico

1. Construir uma linha de base reproduzível para Python, PySpark e dbt.
2. Configurar checks locais e remotos adequados a cada tecnologia.
3. Injetar uma falha conhecida por vez, em branch experimental isolada.
4. Observar o primeiro detector na CI e executar oráculo integral quando a CI passar.
5. Registrar resultado, duração, limitações e comparar as tecnologias.

## Controles de validade

- A tag `baseline-ci-v1` fixa o ponto de partida.
- Código defeituoso nunca é integrado ao `main`.
- Resultado esperado (catálogo) e resultado observado (CSV) são separados.
- Falsos negativos são confirmados por oráculo de dados independente.

O procedimento executável está no [[../20 - Execução/Protocolo de falhas controladas|protocolo de falhas controladas]].
