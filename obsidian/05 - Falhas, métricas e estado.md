# Falhas, métricas e estado

Uma falha é uma mutação mínima, deliberada e rastreável. `detected` significa que a esteira bloqueou; `false_negative` significa que a CI passou e um oráculo da execução integral revelou o efeito.

## Estado

- **Python:** PY-001 a PY-005 concluídas; cinco detecções.
- **PySpark:** SP-001 a SP-005 concluídas; três detecções e dois falsos negativos (schema e join).
- **dbt:** DBT-001 a DBT-005 catalogadas; a rodada ainda não está consolidada.

## Medidas

1. taxa de detecção;
2. duração da esteira/checks;
3. nível de adaptação por tecnologia;
4. estabilidade, quando aplicável.

Os números canônicos estão em [[../results/resultados.csv|resultados.csv]]. Definição esperada e observado devem ser distinguidos por meio do [[../fault-catalog/falhas.yml|catálogo]] e do [[../docs/registro-metodologico|registro]].
