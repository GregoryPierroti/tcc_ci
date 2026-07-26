# Fluxo de checks do ETL PySpark

O workflow `CI - ETL PySpark` executa, nesta ordem: formatação, lint, testes
Spark determinísticos com cobertura e auditoria de dependências. Uma falha
bloqueia as etapas seguintes; o encerramento dos recursos Docker ainda é
executado.

## Evidência da rodada inicial

| Falha | Primeiro detector observado | Etapa | Duração |
| --- | --- | --- | --- |
| SP-001, normalização | pytest | Executar testes Spark determinísticos | 73 s |
| SP-002, coluna inexistente | pytest | Executar testes Spark determinísticos | 62 s |
| SP-003, schema de CNPJ | nenhum na CI basal | fora da CI basal | 49 s |
| SP-004, tipo de join | nenhum na CI basal | fora da CI basal | 55 s |
| SP-005, lockfile inválido | uv | Verificar formatação | 31 s |

SP-003 e SP-004 passaram pelos checks da esteira, mas a execução integral
detectou, respectivamente, delivery vazio (0 em vez de 154 linhas) e aumento
indevido de cardinalidade (1589 em vez de 154 linhas). São, portanto, falsos
negativos deliberadamente documentados, não resultados inconclusivos.

SP-005 confirmou que `uv sync --frozen` consome o `uv.lock`: a mutação deve
atingir o lockfile, e não apenas o `pyproject.toml`, para testar a resolução de
dependências reproduzível.

## Limite de interpretação

Os resultados demonstram a detecção ou a lacuna das mutações específicas. A
CI ainda não executa a validação de cardinalidade e integridade de chaves da
execução integral; essa é a principal melhoria a avaliar antes de tratar a
esteira como proteção suficiente para transformações de join e schema.
