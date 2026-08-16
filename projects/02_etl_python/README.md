# ETL Python

Este projeto executa um fluxo local de dados nas camadas `raw`, `trusted` e
`delivery`. Os dados de entrada versionados em `src/pipeline/Dados/` são
enviados para um armazenamento S3 compatível (MinIO), ingeridos no PostgreSQL,
transformados e unidos na tabela final `delivery.bancos_unificados`.

## Pré-requisitos

- Docker com Docker Compose v2;
- `make` (opcional; os comandos equivalentes são mostrados no `Makefile`).

## Execução local

1. Crie o ambiente local a partir do exemplo:

   ```sh
   cp .env.example .env
   ```

2. Execute o fluxo completo:

   ```sh
   make run
   ```

3. Verifique as tabelas criadas:

   ```sh
   make status
   ```

4. Execute os testes locais determinísticos:

   ```sh
   make test
   ```

O Compose declara PostgreSQL, MinIO, criação do bucket e os schemas de banco.
Não são necessárias credenciais AWS, banco remoto ou dados externos.

## Verificações locais de qualidade

```sh
make format-check  # confirma a formatação com Ruff
make docformat-check # confirma a formatação das docstrings
make lint            # verifica código, imports e padrões propensos a defeito
make type-check      # verifica contratos estáticos com mypy
make complexity      # reporta complexidade ciclomática com Radon
make dead-code       # procura código não utilizado com Vulture
make architecture    # impede dependência da infraestrutura para a orquestração
make test-unit       # executa os testes unitários isolados (cobertura >= 95% de pipeline)
make test-integration # executa integrações técnicas com PostgreSQL e MinIO
make test            # executa as duas camadas de teste
make security        # executa Bandit e audita dependências instaladas
make sbom            # gera inventário CycloneDX das dependências Python
```

As dependências e configurações Python estão em `pyproject.toml`; `uv.lock`
congela a resolução usada pelo Docker.

## Reexecução limpa

Para remover somente os volumes locais deste projeto e executar novamente do
zero, use:

```sh
make reset
make run
```

`make reset` apaga os dados locais de PostgreSQL e MinIO deste Compose.
