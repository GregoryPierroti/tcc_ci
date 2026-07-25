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

O Compose declara PostgreSQL, MinIO, criação do bucket e os schemas de banco.
Não são necessárias credenciais AWS, banco remoto ou dados externos.

## Reexecução limpa

Para remover somente os volumes locais deste projeto e executar novamente do
zero, use:

```sh
make reset
make run
```

`make reset` apaga os dados locais de PostgreSQL e MinIO deste Compose.
