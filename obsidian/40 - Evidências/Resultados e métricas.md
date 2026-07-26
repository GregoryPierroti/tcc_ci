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
| dbt | 5 | 5 | 0 | concluída |

Os falsos negativos PySpark são informação metodológica relevante: SP-003
quebrou a chave e produziu delivery vazio; SP-004 aumentou a cardinalidade.
Ambas passaram pela CI basal e só foram reveladas pela execução integral.

## Síntese final da rodada

Foram registradas 15 execuções: 13 detecções na CI e dois falsos negativos,
ambos em PySpark. A taxa global observada é 86,7%. A duração média dos
workflows foi 18,0 s (Python), 54,0 s (PySpark) e 69,2 s (dbt); esses valores
incluem o ambiente da CI e não são benchmarks de produção.

A [[Matriz comparativa final|matriz final das 15 execuções]] detalha cada execução,
as adaptações por tecnologia e a leitura adequada das taxas. A
[[Interpretação comparativa|discussão e limites dos resultados]] separa os achados que
os dados sustentam de seus limites metodológicos.

## Evidência canônica

- [[../../results/resultados.csv|dados brutos em CSV]]: valores por execução e URL de job.
- [[Catálogo de falhas|catálogo das mutações]]: mutação e expectativa.
- [[../50 - Storytelling/Registro metodológico|diário metodológico]]: justificativa e limitações.
- [[Rastreabilidade das evidências|guia de rastreabilidade]]: caminho de auditoria entre as fontes.
