# Fluxo de checks do ETL Python

O workflow `CI - ETL Python` executa, nesta ordem: formatação, lint, testes
determinísticos com cobertura e auditoria de dependências. Cada etapa é
bloqueante; após uma falha, as etapas seguintes são ignoradas e o encerramento
dos recursos Docker ainda é executado.

## Evidência da rodada inicial

| Falha | Primeiro detector observado | Etapa | Duração |
| --- | --- | --- | --- |
| PY-001, sintaxe | Ruff format | Verificar formatação | 22 s |
| PY-002, transformação | pytest | Executar testes determinísticos | 20 s |
| PY-003, filtro de join | pytest | Executar testes determinísticos | 18 s |
| PY-004, coluna inexistente | pytest | Executar testes determinísticos | 22 s |
| PY-005, lockfile inválido | uv | Verificar formatação | 8 s |

PY-001 mostrou que o formatador Ruff também faz parse e pode detectar sintaxe
antes do lint. PY-005 mostrou que `uv sync --frozen` consome o `uv.lock`; por
isso uma alteração isolada no `pyproject.toml` não é um teste válido de
resolução de dependências nesse objeto.

## Limite de interpretação

Os resultados demonstram detecção das mutações específicas, não uma garantia
geral de qualidade. Cobertura permanece métrica auxiliar, e o workflow não
executa a integração completa do ETL nesta rodada.
