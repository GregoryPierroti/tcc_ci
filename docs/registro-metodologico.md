# Registro metodológico e diário de decisões

Este documento registra, em ordem cronológica, decisões, etapas executadas,
evidências e mudanças relacionadas ao experimento do TCC. Ele é a fonte de
rastreabilidade para a redação posterior da metodologia da monografia.

## Convenções

- Cada entrada recebe um identificador sequencial (`DEC`, `ETP` ou `EVD`).
- Decisões ainda não aprovadas permanecem com o estado **em discussão**.
- Alterações de código, infraestrutura ou configuração devem indicar arquivos,
  comandos de verificação e resultado.
- Não registrar credenciais, valores de `.env` ou outros segredos.

## Registro

### 2026-07-25 — DEC-001 — Registro metodológico obrigatório

- **Estado:** decidido.
- **Decisão:** registrar neste arquivo toda decisão e etapa relevante realizada
  a partir desta data no preparo e na execução do experimento.
- **Local escolhido:** `tcc_ci/docs/registro-metodologico.md`.
- **Justificativa:** separar a documentação metodológica dos objetos
  experimentais e manter um histórico único, versionável e citável.
- **Impacto:** antes de cada alteração material, será adicionada uma entrada com
  objetivo, escopo, arquivos afetados, verificação e resultado.

### 2026-07-25 — DEC-002 — Escopo da etapa atual

- **Estado:** decidido.
- **Decisão:** a primeira etapa prática será recuperar, organizar e validar a
  execução local dos projetos `02_ETL_python`, `03_ETL_Pyspark` e
  `04_ETL_dbt`.
- **Inclui:** organização mínima, revisão/criação de Dockerfiles e Compose,
  configuração reproduzível e validação de execução dos três projetos.
- **Não inclui:** implementação de CI, pipelines, templates de CI ou injeção de
  falhas experimentais.
- **Critério de saída proposto:** cada projeto possui instruções locais claras,
  infraestrutura declarada no repositório e uma execução basal verificável.

### 2026-07-25 — DEC-003 — Organização dos repositórios

- **Estado:** decidido.
- **Premissa confirmada:** o repositório
  `eEDB011ingestao_dados_grupo_d`, que contém os três ETLs originais, serve
  exclusivamente como fonte de consulta. Ele não será o local de mudanças do
  experimento.
- **Decisão:** usar `tcc_ci` como monorepo experimental e preservar o
  repositório de origem inalterado.
- **Justificativa:** há um único protocolo, uma única evolução metodológica e
  resultados comparáveis; a cópia inicial cria uma linha de base experimental
  explícita sem alterar a fonte.
- **Estrutura-alvo inicial:** `projects/02_etl_python`,
  `projects/03_etl_pyspark` e `projects/04_etl_dbt`; além de `docs/`,
  `fault-catalog/`, `results/` e `scripts/` na raiz do monorepo.
- **Consequência:** qualquer recuperação, organização, Docker/IaC e validação
  de execução ocorrerá nas cópias experimentais dentro de `tcc_ci`.

### 2026-07-25 — DEC-004 — Dados versionados para execução demonstrável

- **Estado:** decidido.
- **Decisão:** cada objeto experimental deve incluir no monorepo os dados de
  entrada mínimos necessários para demonstrar sua execução local.
- **Política:** CSV, TSV, Parquet ou outros arquivos pequenos, determinísticos
  e sem dados sensíveis podem ser versionados em diretórios explicitamente
  identificados como dados de exemplo ou fixture.
- **Exclusões:** saídas produzidas na execução, logs, diretórios temporários,
  caches, `target/` de dbt e Parquet gerado não serão versionados, exceto se um
  arquivo for deliberadamente escolhido como dado de entrada de referência.
- **Justificativa:** o projeto deve ser demonstrável e reproduzível sem acesso
  a S3, banco remoto ou fontes externas.

### 2026-07-25 — DEC-005 — Política de commits

- **Estado:** decidido.
- **Decisão:** o agente prepara e cria os commits do monorepo `tcc_ci` ao fim
  de cada unidade coerente de trabalho validada.
- **Regras:** um commit deve ter escopo único, mensagem descritiva em formato
  convencional, registro metodológico atualizado e apenas arquivos diretamente
  relacionados à etapa. Segredos e arquivos gerados não entram em commits.
- **Validação:** antes de cada commit, inspecionar o diff e executar as
  verificações que já existirem e forem pertinentes; o resultado será anotado
  neste documento.
- **Exemplo de mensagem:** `chore(baseline): import python etl source`.

### 2026-07-25 — DEC-006 — Ordem de trabalho por objeto experimental

- **Estado:** decidido.
- **Decisão:** cada ETL será tratado individualmente na seguinte ordem:
  1. importar e inventariar a linha de base;
  2. revisar código, dados, dependências e infraestrutura declarada;
  3. registrar a execução basal e seus bloqueios;
  4. realizar apenas as correções necessárias para execução local reproduzível;
  5. validar uma execução completa com dados versionados;
  6. registrar evidências e criar o commit da etapa.
- **Aplicação inicial:** iniciar pelo `02_etl_python`; somente após sua
  validação seguir para `03_etl_pyspark` e, depois, `04_etl_dbt`.
- **Critério:** uma alteração não é considerada concluída apenas porque o
  Docker constrói; deve haver uma execução observável com saída verificável.
