# Resultados e métricas

## Medidas

1. taxa de detecção: falhas detectadas ÷ falhas introduzidas;
2. duração total do job e dos checks;
3. adaptação: direta, configurada, complementar ou não aplicável;
4. estabilidade, quando houver reexecuções comparáveis.

## Resultado consolidado até agora

| Tecnologia | Falhas executadas | Detectadas | Falsos negativos | Situação |
| --- | ---: | ---: | ---: | --- |
| Python | 5 | 5 | 0 | concluída |
| PySpark | 5 | 3 | 2 | concluída |
| dbt | 0 | — | — | pendente |

Os falsos negativos PySpark são informação metodológica relevante: SP-003
quebrou a chave e produziu delivery vazio; SP-004 aumentou a cardinalidade.
Ambas passaram pela CI basal e só foram reveladas pela execução integral.

## Evidência canônica

- [[../../results/resultados.csv|CSV]]: valores por execução e URL de job.
- [[Catálogo de falhas]]: mutação e expectativa.
- [[../50 - Storytelling/Registro metodológico|Registro]]: justificativa e limitações.
