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

### 2026-07-25 — ETP-001 — Importação da linha de base do ETL Python

- **Estado:** concluída.
- **Objetivo:** criar uma cópia experimental rastreável do objeto
  `02_ETL_python`, sem alterar a fonte.
- **Origem:**
  `eEDB011ingestao_dados_grupo_d/02_ETL_python`, no commit fonte
  `f0fceafc95cc9c848ce8ca3def6f73208383d806` (árvore de trabalho limpa).
- **Destino:** `projects/02_etl_python/` no monorepo `tcc_ci`.
- **Conteúdo importado:** 21 arquivos (368 KB), incluindo código Python,
  Dockerfile/Compose, requisitos e os dados CSV/TSV de entrada disponíveis.
- **Exclusões:** não havia artefatos gerados, credenciais ou diretórios Git no
  conteúdo importado.
- **Verificação:** `diff -qr` entre origem e destino não apresentou diferenças.
- **Próxima etapa:** revisão técnica da cópia basal; nenhuma correção foi feita
  nesta importação.

### 2026-07-25 — ETP-002 — Revisão basal do ETL Python

- **Estado:** concluída.
- **Fluxo identificado:** arquivos locais em `src/pipeline/Dados/` são enviados
  a S3, ingeridos para PostgreSQL na camada `raw`, transformados para
  `trusted` e unidos em `delivery`.
- **Dados:** os CSV/TSV importados são entradas reais do fluxo e seus formatos
  correspondem às categorias Bancos (TSV), Empregados (CSV separado por `|`) e
  Reclamações (CSV separado por `;`, codificação Latin-1). O arquivo
  `2022_tri_02_nao_ha_dados.csv` é vazio.
- **Bloqueio reproduzido:** `docker compose config` falha porque o arquivo
  `.env` referenciado não existe.
- **Bloqueios adicionais identificados:** o Compose solicita `Dockerfile`, mas
  a cópia contém `dockerfile`; ele não declara PostgreSQL; o código exige S3,
  PostgreSQL e schemas `raw`, `trusted` e `delivery` externos; `main.py`
  sempre tenta enviar os dados ao S3.
- **Defeitos de recuperação relevantes:** o processamento retorna da categoria
  inteira ao encontrar arquivo vazio (`ingestao_raw.py`); as configurações de
  separador calculadas ali não são usadas; e uma nova execução pode acumular
  dados em `raw`.
- **Decisão de recuperação:** declarar uma infraestrutura local em Docker
  Compose com PostgreSQL, MinIO (S3 compatível), inicialização de bucket e
  criação dos schemas. A aplicação continuará usando o fluxo S3/PostgreSQL,
  sem credenciais de cloud nem serviços externos.
- **Critério de validação posterior:** uma execução limpa deve produzir as
  tabelas `raw.*`, `trusted.*` e `delivery.bancos_unificados` no PostgreSQL
  local, com contagens registradas.

### 2026-07-25 — ETP-003 — Recuperação e validação local do ETL Python

- **Estado:** concluída.
- **Infraestrutura declarada:** `Dockerfile`, `docker-compose.yaml`,
  `infra/postgres/init.sql`, `.env.example`, `.dockerignore` e `Makefile`.
  O Compose sobe PostgreSQL 16, MinIO e um inicializador de bucket antes da
  aplicação.
- **Dependências:** `requirements.txt` passou a usar versões fixadas; `s3fs`,
  que não era importada pelo projeto e tornava a resolução do `pip` instável,
  foi removida.
- **Correções de execução:** arquivos de entrada vazios são ignorados no envio
  e na ingestão; a ingestão substitui a tabela `raw` no primeiro arquivo de
  cada categoria e acrescenta os demais, evitando acúmulo entre execuções.
- **Comando de validação:** após `docker compose down -v`, foi executado
  `make run`, que cria os serviços, o bucket e executa a aplicação. A consulta
  posterior foi feita no PostgreSQL local.
- **Resultado da execução limpa:** 10 arquivos não vazios enviados;
  `raw.reclamacoes` e `trusted.reclamacoes` com 918 linhas; `raw.bancos` e
  `trusted.bancos` com 1474 linhas; `raw.empregados` e `trusted.empregados`
  com 39 linhas; `delivery.bancos_unificados` com 11 linhas e 3 CNPJs
  distintos.
- **Reprodutibilidade:** uma segunda execução sem limpeza preservou 918 linhas
  em `raw.reclamacoes` e 11 registros em `delivery.bancos_unificados`.
- **Instruções ao usuário:** `README.md` documenta `make run`, `make status` e
  `make reset`. O último remove somente os volumes Docker locais deste projeto.

### 2026-07-25 — ETP-004 — Importação da linha de base do ETL PySpark

- **Estado:** concluída.
- **Objetivo:** criar a cópia experimental do objeto `03_ETL_Pyspark` sem
  alterar o repositório-fonte.
- **Origem:** `eEDB011ingestao_dados_grupo_d/03_ETL_Pyspark`, no commit fonte
  `f0fceafc95cc9c848ce8ca3def6f73208383d806` (árvore de trabalho limpa).
- **Destino:** `projects/03_etl_pyspark/` no monorepo `tcc_ci`.
- **Conteúdo importado:** 20 arquivos (352 KB), incluindo código, Docker,
  requisitos e dados de entrada CSV/TSV.
- **Exclusões justificadas:** `src/pipeline/Camadas/` não foi copiado. Ele
  continha Parquets, `_SUCCESS` e arquivos `.crc` gerados por Spark, que são
  resultados de execução e serão recriados localmente.
- **Verificação:** `diff -qr`, excluindo apenas `Camadas/`, não apresentou
  diferenças entre a fonte e o destino.
- **Próxima etapa:** revisão técnica da cópia basal, sem correções nesta etapa.

### 2026-07-25 — ETP-005 — Revisão basal do ETL PySpark

- **Estado:** concluída.
- **Fluxo identificado:** arquivos locais em `src/pipeline/Dados/` são lidos
  pelo Spark, materializados em Parquet nas camadas `RAW`, `Trusted` e
  `Delivery`, e a tabela final é escrita no PostgreSQL por JDBC.
- **Bloqueio reproduzido:** `docker compose config` não é válido sem `.env` e
  emite variáveis PostgreSQL vazias; o arquivo referenciado como Dockerfile não
  existe, pois a fonte contém `dockerfile`.
- **Bloqueios adicionais identificados:** `main.py` fixa `/app/src`; o Compose
  mantém o contêiner inativo (`tail -f /dev/null`) em vez de executar o ETL; a
  sessão Spark solicita o driver JDBC por `spark.jars.packages`, criando uma
  dependência de rede; e as exceções principais são apenas registradas, sem
  retornar código de falha.
- **Dados e artefatos:** Bancos é TSV, Empregados usa `|` e Reclamações usa
  `;` com codificação Latin-1; o arquivo de reclamações de 2022-T2 é vazio.
  `Camadas/` é saída gerada pelo Spark, não fonte.
- **Decisão de recuperação:** declarar um ambiente local composto por Spark
  local (PySpark 3.5 e Java 17) e PostgreSQL, com driver JDBC instalado na
  imagem e referenciado localmente. Preservar Parquet como saída intermediária,
  mas ignorá-lo no Git.
- **Critério de validação posterior:** uma execução limpa deve recriar as três
  camadas Parquet e a tabela PostgreSQL `reclamacoes_consolidadas`, com
  contagens registradas e status de processo bem-sucedido.

### 2026-07-25 — ETP-006 — Recuperação e validação local do ETL PySpark

- **Estado:** concluída.
- **Infraestrutura:** Docker Compose com PostgreSQL 16; imagem Python 3.11
  Bookworm, Java 17, PySpark 3.5 e driver JDBC PostgreSQL instalado na imagem.
- **Correções:** execução direta via `make run`, caminhos parametrizáveis,
  exceções propagadas, schema CSV com 15 colunas e limpeza de `Camadas/` antes
  de cada execução. Artefatos Parquet são ignorados no Git.
- **Evidência:** em execução limpa, a tabela
  `reclamacoes_consolidadas` possui 154 registros e 38 CNPJs distintos; a
  saída RAW de Bancos contém um único arquivo Parquet, sem resíduo de runs.

### 2026-07-25 — DEC-007 — Estratégia de branches

- **Estado:** decidido.
- **Decisão:** `main` representa o estado integrado e estável; cada recuperação
  ocorre em uma feature branch e é integrada explicitamente após validação.

### 2026-07-25 — ETP-007 — Preparação de publicação no GitHub

- **Estado:** concluída.
- **Ação:** GitHub CLI oficial instalado localmente em `tools/gh`; credenciais
  não são versionadas.

### 2026-07-25 — ETP-008 — Publicação e integração no GitHub

- **Estado:** concluída.
- **Publicação:** `main`, `feat/etl-python-local` e
  `feat/etl-pyspark-local` foram enviados ao remoto.
- **PRs:** PR #1 (Python) e PR #2 (PySpark) foram integrados em `main` com
  commits de merge após resolução dos conflitos documentais.

### 2026-07-25 — ETP-009 — Importação da linha de base do ETL dbt

- **Estado:** concluída.
- **Branch:** `feat/etl-dbt-local`.
- **Origem:** `eEDB011ingestao_dados_grupo_d/04_ETL_dbt`, commit fonte
  `f0fceafc95cc9c848ce8ca3def6f73208383d806`.
- **Destino:** `projects/04_etl_dbt/` (48 arquivos, 796 KB).
- **Exclusões:** `dbt/project/target/`, `dbt/project/logs/` e o perfil
  específico de usuário `dbt/profiles/.user.yml`; são artefatos ou configuração
  local não reproduzível.
- **Próxima etapa:** revisar raiz do projeto dbt, Compose, perfil, seeds e
  dependências antes de qualquer correção.

### 2026-07-25 — ETP-010 — Recuperação e validação local do ETL dbt

- **Estado:** concluída.
- **Problemas basais confirmados:** o Compose montava `dbt/project` em
  `/app`, mas `dbt_project.yml` estava fora desse diretório; o Dockerfile era
  referenciado como `Dockerfile`, embora existisse como `dockerfile`; o perfil
  apontava a camada local para `warehouse`, enquanto os `source()` declaravam
  o banco `postgres`; e o delivery tratava modelos internos como fontes
  externas (`source()`) em vez de dependências dbt (`ref()`).
- **Infraestrutura recuperada:** a raiz única do projeto passou a ser
  `dbt/project/`, com `dbt_project.yml` nesse diretório; `dbt/Dockerfile` usa
  Python 3.11, git, dbt-core 1.9.0 e dbt-postgres 1.9.0; Docker Compose
  declara PostgreSQL 16 e injeta as variáveis de conexão no perfil dbt.
  Foram adicionados `.env.example`, `.gitignore`, `Makefile` e `README.md`.
- **Decisão de execução:** `make run` executa `dbt seed --full-refresh` antes
  de `dbt build`. Os modelos dependem de entradas declaradas por `source()`,
  cuja criação pelos seeds não forma uma dependência de grafo dbt; portanto a
  ordem explícita evita corrida em banco vazio.
- **Correções de modelos:** `mod_final.sql` passou a usar `ref()` para
  `mod_bancos`, `mod_reclamacoes` e `mod_empregados`; os sources de entrada
  passaram a apontar para `warehouse.public`; as três fontes `public_trusted`
  obsoletas foram removidas. Em `mod_bancos`, a chave incremental passou a
  ser `(cnpj, segmento, nome)`, após a descoberta de colisões em
  `nome_processed`; o `SELECT DISTINCT` da staging preserva linhas com nome
  original diferente e elimina somente duplicatas literais.
- **Falhas encontradas durante a validação:** a primeira imagem não continha
  git, exigido por `dbt debug`; a primeira construção falhou porque os sources
  compilavam para `postgres.public`; e a segunda construção revelou que a
  chave incremental anterior não era única (`MERGE command cannot affect row
  a second time`). Todas foram reproduzidas localmente e corrigidas antes da
  validação final.
- **Validação final:** após `make reset` (somente o volume PostgreSQL local),
  `make debug`, `make parse`, `make run` e uma segunda execução de
  `make build` concluíram com sucesso. Cada build processou 26 nós: 10 seeds
  e 16 modelos, sem avisos ou erros. `dbt ls --resource-type source` encontrou
  os 10 sources reais dos seeds (1 de bancos, 2 de empregados e 7 de
  reclamações). A conexão em `warehouse.public` foi aprovada por `dbt debug`.
- **Saída observada:** `public_trusted.mod_bancos` tem 1474 linhas,
  `public_trusted.mod_reclamacoes` 918, `public_trusted.mod_empregados` 39 e
  `public_delivery.mod_final` 1. A segunda execução preservou o resultado de
  delivery com 1 linha, comprovando a reexecução local para os dados atuais.

### 2026-07-25 — ETP-011 — Integração da recuperação dbt

- **Estado:** concluída.
- **Pull request:** [#3](https://github.com/GregoryPierroti/tcc_ci/pull/3),
  aberto a partir de `feat/etl-dbt-local` e integrado por merge em `main`.
- **Critério atendido:** o PR estava `CLEAN` e `MERGEABLE`; a integração só
  ocorreu depois das validações locais descritas na ETP-010.

### 2026-07-25 — DEC-008 — Consolidação da linha de base experimental

- **Estado:** decidido e em execução na branch `feat/experiment-baseline`.
- **Escopo:** padronizar a documentação e os comandos locais, registrar
  runtimes e oráculos observáveis e adicionar testes mínimos determinísticos
  aos três objetos. Nenhum workflow, arquivo de CI ou execução remota será
  introduzido nesta etapa.
- **Decisão comparativa:** preservar as regras de negócio e as contagens de
  delivery já recuperadas. As saídas de Python (11), PySpark (154) e dbt (1)
  não serão artificialmente igualadas, pois os joins e recortes originais são
  diferentes; a equivalência será avaliada por oráculos internos a cada
  objeto.
- **Entregável:** `docs/baseline-experimental.md`, comandos `make test` e uma
  execução local documentada dos testes.

### 2026-07-25 — DEC-009 — Oráculos locais mínimos

- **Estado:** decidido e em validação.
- **Python:** testes unitários da normalização de nomes e da agregação delivery
  com um adaptador de banco em memória; não exige PostgreSQL ou MinIO ativos.
- **PySpark:** testes em `local[2]` da normalização e da escrita/leitura
  Parquet com fixture temporária; não exige cluster nem JDBC.
- **dbt:** teste singular SQL de contagens basais das três relações trusted e
  da relação delivery. O alvo `make test` prepara o banco local antes de rodar
  o teste, de modo que pode ser executado de forma isolada.
- **Limite explícito:** esses oráculos comprovam a linha de base atual e não
  são, ainda, uma cobertura ampla de regras de negócio ou uma pipeline de CI.

### 2026-07-25 — ETP-012 — Defeito de normalização Spark encontrado por teste local

- **Estado:** corrigido, pendente de revalidação.
- **Evidência:** o teste da entrada `Banco Itaú S.A.` produziu `ITAU SA`, não
  `ITAU`. A ordem existente remove a pontuação antes de aplicar os padrões, de
  modo que `S.A.` se torna `SA`; esse token não estava na lista de remoção.
- **Correção:** incluir `SA` na lista de padrões de
  `TransformacoesTrustedSpark._criar_chave_nome`. A mudança implementa a
  intenção explícita de remover sufixos societários, sem ampliar o escopo da
  regra de negócio.

### 2026-07-25 — ETP-013 — Validação da linha de base experimental

- **Estado:** concluída.
- **Testes locais:** `02_etl_python` passou com 3 testes pytest;
  `03_etl_pyspark` passou com 2 testes pytest em Spark `local[2]`; e
  `04_etl_dbt` passou com o teste singular `baseline_counts`.
- **dbt:** `make test` executou `seed`, `build` e `dbt test`; o build passou
  27 nós (10 seeds, 16 modelos e 1 teste) e o teste isolado também passou.
- **Execução integral Python:** após `make reset` e `make run`, foram
  observadas 1474 linhas de bancos, 918 de reclamações, 39 de empregados, 154
  correspondências intermediárias e 11 linhas em
  `delivery.bancos_unificados`.
- **Execução integral PySpark:** após `make reset` e `make run`, a tabela
  `reclamacoes_consolidadas` teve 154 linhas. A correção de `SA` não alterou
  essa contagem basal.
- **Limitação observada:** Spark emite avisos de divergência nominal entre o
  schema sem acentos e o cabeçalho CSV com acentos. A leitura com schema
  explícito, o build e os oráculos passaram; o aviso fica registrado para uma
  futura análise de qualidade, sem alterar a estrutura de dados nesta fase.
- **Ambiente:** os contêineres foram encerrados com `make down`/`docker compose
  down`, preservando os volumes locais; nenhum dado versionado ou artefato de
  execução entrou no repositório.

### 2026-07-25 — ETP-014 — Integração da linha de base experimental

- **Estado:** concluída.
- **Pull request:** [#4](https://github.com/GregoryPierroti/tcc_ci/pull/4),
  integrado por merge em `main` após confirmação de estado `CLEAN` e
  `MERGEABLE`.
- **Resultado:** `main` passa a conter os três ETLs executáveis localmente,
  seus oráculos mínimos e a documentação da linha de base. A próxima fase é a
  primeira esteira de CI, que chamará os comandos locais já validados.

### 2026-07-25 — DEC-010 — Ferramentas da preparação local de qualidade

- **Estado:** decidido e em execução na branch `feat/local-quality-checks`.
- **Python e PySpark:** `pyproject.toml` será a fonte de metadados e
  configuração; `uv.lock` congelará a resolução das dependências; Ruff fará
  verificação de formatação, lint e ordenação de imports; pytest continuará
  sendo o executor de testes; e `pip-audit` será exposto como verificação de
  dependências.
- **dbt:** o projeto manterá `dbt_project.yml` e as versões no Dockerfile;
  SQLFluff será instalado na mesma imagem para lint SQL com o dialect Postgres
  e o templater dbt já declarados.
- **Interface comum:** cada Makefile receberá alvos explícitos de
  `format-check`, `lint` e, nos projetos Python, `security`. A execução de
  produção continua em `make run` e nenhum workflow de CI será criado nesta
  decisão.
- **Escopo:** não adotar mypy, pre-commit ou templates de workflow nesta fase.

### 2026-07-25 — ETP-015 — Preparação local de qualidade e revalidação

- **Estado:** concluída, pendente apenas de revisão e integração por pull
  request.
- **Reprodutibilidade Python/PySpark:** os dois objetos passaram a declarar
  dependências em `pyproject.toml` e resolução exata em `uv.lock`. Os antigos
  `requirements.txt` foram removidos para evitar duas fontes divergentes de
  dependência. As imagens Docker usam `uv sync --frozen`, portanto a mesma
  resolução é empregada localmente e na futura CI.
- **Segurança:** a primeira execução de `pip-audit --strict` no ETL Python
  encontrou `PYSEC-2026-1845` em `pytest 8.3.4` e `PYSEC-2026-2270` em
  `python-dotenv 1.0.1`. Foram adotadas as correções disponíveis (`pytest
  9.0.3` nos dois objetos e `python-dotenv 1.2.2` no Python), locks foram
  regenerados e as auditorias posteriores passaram sem vulnerabilidades
  conhecidas.
- **Qualidade Python:** `make format-check`, `make lint`, `make test` e
  `make security` passaram. Ruff aplicou apenas formatação, ordenação de
  imports e a remoção de construções equivalentes; os três testes continuam
  verdes. A montagem do código foi deslocada para `/app/src` para não ocultar
  o `pyproject.toml` e o ambiente virtual da imagem; os dados continuam
  montados em `/app/Dados`, caminho requerido pela execução existente.
- **Qualidade PySpark:** os mesmos quatro comandos passaram, com dois testes
  Spark em `local[2]`. Três lambdas usadas somente como leitores foram
  convertidas em funções nomeadas pelo lint, sem mudança de schema ou de
  transformação. A execução integral inicialmente não resolvia `postgres`
  porque `make run` usava `docker compose run --no-deps`; o alvo agora mantém
  a rede Compose e voltou a gravar 154 registros. Python, PySpark e dbt usam a
  porta local 5432, logo seus serviços devem ser encerrados entre execuções;
  isso é uma limitação operacional documentada, não uma dependência externa.
- **Qualidade dbt/SQL:** SQLFluff 3.3.1 e o templater dbt foram incluídos na
  imagem. Foram aplicadas 210 correções automáticas exclusivamente de layout
  aos modelos. `RF02` (qualificação de referências) e `ST06` (ordem de
  colunas) foram explicitamente excluídas do conjunto inicial por exigirem
  revisão semântica; a exclusão será reavaliada ao definir as falhas
  experimentais. Após isso, `make lint` passou e `make test` concluiu 27 itens
  dbt, incluindo o teste singular basal.
- **Limite de escopo:** não foi criado workflow de CI, relatório remoto ou
  check automático de pull request. Esta etapa apenas consolidou comandos
  locais bloqueantes que a próxima etapa de CI chamará.

### 2026-07-25 — ETP-016 — Integração dos checks locais de qualidade

- **Estado:** concluída.
- **Pull request:** [#5](https://github.com/GregoryPierroti/tcc_ci/pull/5),
  aberto a partir de `feat/local-quality-checks` e integrado por merge em
  `main` após confirmação de estado `CLEAN` e `MERGEABLE`.
- **Resultado:** a `main` contém a interface local comum de qualidade e as
  respectivas versões de dependências congeladas. A imagem de diagrama anexada
  manualmente na raiz do repositório foi preservada como arquivo não rastreado
  e não compõe este commit nem o PR.

### 2026-07-25 — DEC-011 — Contrato operacional e revisão de pull requests

- **Estado:** decidido e em implementação na branch `docs/project-workflow`.
- **Decisão:** versionar `AGENTS.md` como contrato operacional do repositório.
  O documento formaliza a autonomia para alterações, validações, commits,
  branches, PRs e merges dentro do escopo do TCC, e preserva as situações que
  ainda exigem direção explícita: segredos, custos externos, ações destrutivas,
  mudança de escopo acadêmico e mudança injustificada de regra de negócio.
- **Rastreabilidade:** todo trabalho relevante deve continuar registrado neste
  diário. O template `.github/pull_request_template.md` torna obrigatório
  descrever objetivo, escopo, validações, registro metodológico e itens fora
  de escopo em cada PR.
- **Justificativa:** a medida reduz a fricção operacional sem tentar substituir
  os controles técnicos do ambiente. Ela também transforma commits e PRs em
  evidências reutilizáveis na redação da metodologia do TCC.

### 2026-07-25 — ETP-017 — Integração do contrato operacional

- **Estado:** concluída.
- **Pull request:** [#6](https://github.com/GregoryPierroti/tcc_ci/pull/6),
  aberto na branch `docs/project-workflow` e integrado por merge em `main`
  após confirmação de estado `CLEAN` e `MERGEABLE`.
- **Resultado:** `AGENTS.md` e o template de PR passam a orientar as próximas
  etapas. A próxima mudança prevista é a branch `feat/ci-python`, dedicada
  exclusivamente à primeira pipeline GitHub Actions do ETL Python.

### 2026-07-25 — DEC-012 — Primeira pipeline GitHub Actions: ETL Python

- **Estado:** decidido e em implementação na branch `feat/ci-python`.
- **Decisão:** criar `.github/workflows/ci-python.yml` como workflow explícito
  do primeiro objeto experimental. Ele dispara em pull requests e pushes para
  `main` que afetem o ETL Python, além de permitir execução manual.
- **Etapas bloqueantes:** preparar um `.env` efêmero a partir de
  `.env.example`, verificar Docker Compose, executar `make format-check`,
  `make lint`, `make test` e `make security`. Os comandos são os mesmos já
  aprovados na validação local, preservando a relação entre ambiente local e
  CI.
- **Isolamento:** a configuração efêmera não contém segredo de produção e é
  descartada com o runner. O encerramento Docker ocorre sempre ao fim do job,
  inclusive em falha.
- **Fora de escopo deliberado:** a primeira versão não executa `make run`,
  não publica artefatos, não mede duração por etapa e não usa cobertura ou
  análise de tipos. Esses elementos serão adicionados somente após confirmar o
  baseline remoto deste workflow, evitando confundir a primeira comparação com
  múltiplas mudanças de uma só vez.

### 2026-07-25 — ETP-018 — Primeira execução remota de CI do ETL Python

- **Estado:** concluída.
- **Pull request:** [#7](https://github.com/GregoryPierroti/tcc_ci/pull/7),
  integrado por merge em `main` após estado `CLEAN` e `MERGEABLE`.
- **Evidência remota:** o job `Qualidade, testes e segurança` do GitHub
  Actions passou em 24 segundos. Foram executados, sem falha, a preparação do
  ambiente efêmero, `make format-check`, `make lint`, `make test` (3 testes) e
  `make security`.
- **Interpretação:** a esteira local escolhida pode ser executada no runner
  hospedado do GitHub sem credenciais externas e bloqueia um pull request se
  qualquer uma de suas quatro verificações falhar. Esse resultado é o baseline
  remoto do objeto Python; ainda não mede cobertura, integração integral ou
  falsos negativos experimentais.

### 2026-07-25 — DEC-013 — Pipeline GitHub Actions: ETL PySpark

- **Estado:** decidido e em implementação na branch `feat/ci-pyspark`.
- **Decisão:** criar `.github/workflows/ci-pyspark.yml`, espelhando o contrato
  de qualidade do objeto Python e usando os comandos já validados do objeto
  PySpark: `make format-check`, `make lint`, `make test` e `make security`.
- **Particularidade tecnológica:** o job executa a imagem Docker que contém
  Python 3.11, Java 17 e PySpark 3.5.2; os testes usam Spark em `local[2]`.
  Por isso, o timeout foi definido em 25 minutos, superior ao do Python, sem
  introduzir cluster ou infraestrutura distribuída.
- **Isolamento:** o workflow cria `.env` a partir de `.env.example`, sem usar
  credenciais externas. A execução integral com PostgreSQL/JDBC (`make run`)
  continua fora do baseline remoto inicial; os testes Spark atuais não exigem
  banco e isolam melhor a avaliação das verificações de qualidade.

### 2026-07-25 — ETP-019 — Atualização de segurança do PySpark

- **Estado:** concluída, pendente de revalidação da branch `feat/ci-pyspark`.
- **Evidência:** `make security` identificou `PYSEC-2025-184` em
  `pyspark 3.5.0`; o banco de vulnerabilidades aponta `3.5.2` como correção
  disponível na linha 3.5.
- **Correção:** atualizar a dependência fixada para `pyspark 3.5.2` e
  regenerar `uv.lock`. Por ser uma atualização de patch de segurança, ela não
  altera deliberadamente a regra de negócio nem o desenho experimental; os
  testes Spark e a auditoria serão repetidos antes de publicar o PR.

### 2026-07-25 — ETP-020 — Primeira execução remota de CI do PySpark

- **Estado:** concluída.
- **Pull request:** [#8](https://github.com/GregoryPierroti/tcc_ci/pull/8),
  integrado por merge em `main` após estado `CLEAN` e `MERGEABLE`.
- **Evidência remota:** o job `Qualidade, testes Spark e segurança` do GitHub
  Actions passou em 1 minuto e 2 segundos. Ele executou a imagem com Java 17 e
  PySpark 3.5.2, format check, lint, 2 testes em Spark `local[2]` e auditoria
  de dependências sem vulnerabilidades conhecidas.
- **Interpretação:** a mesma esteira convencional de qualidade usada no ETL
  Python é aplicável ao PySpark com adaptação limitada ao runtime Java/Spark.
  O aumento de duração observado (24 segundos no Python; 62 segundos no
  PySpark) é uma primeira evidência de custo adicional do ambiente Spark, e
  não uma medida final de desempenho.

### 2026-07-25 — DEC-014 — Pipeline GitHub Actions: ETL dbt

- **Estado:** decidido e em implementação na branch `feat/ci-dbt`.
- **Decisão:** criar `.github/workflows/ci-dbt.yml` para executar `make lint`
  (SQLFluff com templater dbt) e `make test` (seeds, `dbt build` e `dbt test`)
  no PostgreSQL efêmero fornecido pelo Docker Compose.
- **Particularidade tecnológica:** dbt não possui testes pytest nem lockfile
  uv neste objeto; as versões de dbt e SQLFluff permanecem explicitamente
  fixadas no Dockerfile. `dbt build` já engloba parse, compilação, materialização
  dos modelos e o teste singular basal, sendo a validação de integração leve
  adequada neste estágio.
- **Segurança:** não será adicionado `pip-audit` à imagem dbt nesta feature.
  A auditoria do conjunto de dependências da imagem requer uma decisão de
  atualização específica para dbt e seus adaptadores, que seria uma variável
  adicional no primeiro baseline remoto. Essa lacuna será registrada como
  limitação comparativa e tratada numa etapa posterior, se mantida no escopo.
- **Isolamento:** o workflow usa apenas `.env.example`, dados versionados e
  PostgreSQL local ao runner; não exige credenciais ou banco externos.

### 2026-07-25 — ETP-021 — Correção mínima após a primeira execução remota do dbt

- **Estado:** concluída localmente; pendente de confirmação pela repetição da
  execução remota da PR #9.
- **Evidência inicial:** a primeira execução do job `SQLFluff e dbt build` da
  PR #9 interrompeu em `int_empregados.sql`. O log reportou duas ocorrências
  de `LT01` (espaçamento excessivo antes de `AS`) e uma exceção interna
  `CV11` (`tuple index out of range`) na linha 42.
- **Diagnóstico:** a reconstrução local sem cache da imagem dbt e uma execução
  com os artefatos `target/` e `logs/` temporariamente removidos não
  reproduziram a exceção CV11; ambos os lints passaram. Portanto, não há
  evidência suficiente para classificar o evento como defeito reproduzível do
  SQLFluff ou para desativar a regra CV11.
- **Correção aplicada:** normalizar exclusivamente os dois espaçamentos de
  `null::text as segmento` em
  `projects/04_etl_dbt/dbt/project/models/trusted/int_empregados.sql`. Não
  houve alteração de expressão SQL, regra de transformação ou modelo dbt.
- **Validação local:** após a correção, `make lint` passou e `make test`
  concluiu o `dbt build` com 27 itens e o teste singular basal aprovados. Os
  serviços efêmeros foram encerrados com `docker compose down`.
- **Interpretação pendente:** a nova execução remota dirá se o evento inicial
  foi transitório ou se ainda existe uma condição não reproduzida localmente;
  mesmo com êxito, a correção de espaçamento não será tomada isoladamente como
  prova causal para a exceção CV11.

### 2026-07-25 — DEC-015 — Supressão localizada de CV11 no modelo dbt

- **Estado:** decidida; pendente da terceira execução remota da PR #9.
- **Evidência adicional:** após a normalização de espaçamento, a segunda
  execução remota da PR #9 voltou a falhar exatamente em
  `int_empregados.sql:42`, com a mesma exceção interna de SQLFluff 3.3.1:
  `CV11` / `tuple index out of range`. O lint local, inclusive com as mesmas
  versões principais de `sqlfluff` (3.3.1), `dbt-core` (1.9.0) e
  `dbt-adapters` (1.16.3), não reproduz a falha.
- **Decisão:** acrescentar `-- noqa: CV11` somente às duas alternativas
  condicionais equivalentes que usam `null::text as segmento`. A própria
  mensagem do SQLFluff indica essa supressão como contorno para a exceção.
- **Justificativa e limite:** a anotação não desativa CV11 globalmente, não
  altera o SQL executado e não encobre outras regras ou outros arquivos. Ela
  torna explícita uma limitação do linter neste padrão de cast, que deverá ser
  considerada ao interpretar as métricas de detecção. A regra permanece ativa
  no restante do projeto.
- **Validação local:** `make lint` passou com as duas supressões; `make test`
  voltou a concluir os 27 itens do `dbt build` e o teste singular basal. Os
  serviços foram encerrados após a validação.

### 2026-07-25 — ETP-022 — Primeira execução remota de CI do dbt

- **Estado:** concluída.
- **Pull request:** [#9](https://github.com/GregoryPierroti/tcc_ci/pull/9),
  integrada por merge em `main` após estado `CLEAN` e `MERGEABLE`.
- **Evidência remota:** a terceira execução do job `SQLFluff e dbt build`
  passou em 1 minuto e 4 segundos. Ela criou o PostgreSQL efêmero, executou o
  lint SQL com templater dbt e concluiu `make test`, que inclui seeds, `dbt
  build` (27 itens) e o teste singular basal.
- **Limitação observada:** as duas tentativas iniciais falharam por exceção
  interna CV11 do SQLFluff no cast condicional `null::text`; a correção de
  espaçamento por si só não resolveu a falha. A supressão de CV11 limitada a
  essas duas linhas foi necessária para a estabilidade no runner hospedado.
  Isso não demonstra falha da transformação nem uma detecção válida de defeito
  de dados; deve ser classificado como limitação da ferramenta/configuração no
  experimento.
- **Baseline comparável:** os três objetos experimentais possuem agora uma
  pipeline GitHub Actions explícita e bloqueante: Python (24 s), PySpark (1
  min 2 s) e dbt (1 min 4 s). A comparação ainda é apenas operacional: dbt
  não possui auditoria de dependências nesta primeira versão, conforme
  DEC-014.

### 2026-07-25 — DEC-016 — Ampliação mínima das verificações para a rodada de falhas

- **Estado:** decidida e em implementação na branch `feat/expanded-validation`.
- **Cobertura Python/PySpark:** incluir `pytest-cov` nos dois projetos e fazer
  o alvo `make test` emitir o resumo no terminal e `coverage.xml`. A cobertura
  será tratada como métrica auxiliar, não como prova de ausência de falhas.
- **dbt visível por etapa:** manter `dbt build` como validação integrada, mas
  executar `dbt parse` e `dbt compile` antes dela como etapas explícitas no
  workflow. Isso permitirá registrar se uma falha de SQL ou de referência foi
  bloqueada durante a análise, compilação ou execução.
- **Testes de schema dbt:** declarar apenas invariantes já sustentadas pelo
  modelo basal: `mod_empregados.employer_sk` obrigatório e único; e
  `mod_final.cnpj` obrigatório. Não serão habilitados contratos dbt agora,
  pois eles exigiriam especificar e manter os tipos de todas as colunas;
  isso aumentaria a mudança simultânea de estrutura e de regra de negócio.
- **Fora de escopo:** `mypy`, auditoria de dependências do dbt e testes
  unitários nativos do dbt continuam pendentes de avaliação posterior. A
  feature atual prioriza detectores diretamente úteis ao catálogo inicial de
  falhas, sem ampliar a plataforma.

### 2026-07-25 — ETP-023 — Validação local das verificações ampliadas

- **Estado:** concluída, pendente de revisão e integração por pull request.
- **Python:** `make test` passou com 3 testes e 32% de cobertura de linhas
  (`coverage.xml` gerado e ignorado pelo Git). Os módulos de ingestão e
  popularização continuam sem cobertura; esse resultado caracteriza o estado
  inicial dos testes, não um limiar de aceite.
- **PySpark:** `make test` passou com 2 testes Spark em `local[2]` e 23% de
  cobertura de linhas. A primeira tentativa foi interrompida durante a
  exportação da imagem Docker, antes dos testes; a repetição com imagem
  disponível passou em 7,05 s de execução de pytest. Trata-se de uma
  intercorrência de ambiente, não de falha do objeto PySpark.
- **dbt:** `make parse`, `make compile` e `make test` passaram. O projeto
  passou a declarar quatro testes de dados: o teste singular basal, `not_null`
  e `unique` para `mod_empregados.employer_sk`, e `not_null` para
  `mod_final.cnpj`. O `dbt build` concluiu 30 itens; o `dbt test` isolado
  concluiu os quatro testes.
- **Próxima validação:** a PR deverá confirmar que os workflows hospedados
  executam a cobertura e as novas etapas dbt com os mesmos comandos locais.

### 2026-07-25 — ETP-024 — Integração das verificações ampliadas

- **Estado:** concluída.
- **Pull request:** [#10](https://github.com/GregoryPierroti/tcc_ci/pull/10),
  integrada por merge em `main` após estado `CLEAN` e `MERGEABLE`.
- **Evidência remota:** todos os workflows passaram com a ampliação: Python
  em 26 s, PySpark em 57 s e dbt em 1 min 18 s. A execução dbt exibiu as
  etapas distintas de lint, parse, compile e build/test; Python e PySpark
  executaram pytest com cobertura.
- **Resultado metodológico:** o baseline agora permite associar falhas a uma
  etapa dbt mais específica e registrar cobertura como métrica auxiliar dos
  objetos Python. A próxima feature deve congelar este baseline e criar o
  catálogo/protocolo de injeção, sem inserir falhas ainda.
