# Guia conceitual de CI e engenharia de dados

## Finalidade deste guia

Este guia sustenta a defesa conceitual da v2. A premissa é que um pipeline de
dados é software que movimenta e transforma dados por meio de código,
configuração, dependências e serviços. Portanto, práticas de engenharia de
software podem reduzir riscos no pipeline. Isso não transforma a esteira em
uma solução de *data quality*: ela não mede nulidade, completude, unicidade ou
correção analítica do conteúdo produzido.

**Integração contínua (CI)** é a execução automatizada e repetível de verificações
em cada mudança, antes que ela seja integrada. Sua função é produzir evidência
rápida sobre a saúde técnica do sistema. No TCC, a CI é avaliada por mutações
controladas: cada mutação representa uma falha técnica plausível e cada
ferramenta é observada quanto à sua capacidade — e aos seus limites — de
detectá-la.

## Princípios que organizam a esteira

| Princípio de engenharia de software | Tradução para pipelines de dados | O que não se conclui |
| --- | --- | --- |
| *Shift left* | Encontrar defeitos de código, configuração e contrato antes de executar um pipeline completo. | Que o dado final está correto. |
| Feedback rápido e em camadas | Checks baratos precedem testes que precisam de Spark, banco ou armazenamento de objetos. | Que a ordem dos checks mede criticidade do defeito. |
| Reprodutibilidade | Dependências travadas, contêineres e bootstrap reduzem variação entre máquina local e CI. | Que a infraestrutura de produção foi validada. |
| Separação de responsabilidades | Orquestração, adaptadores e regras de infraestrutura têm fronteiras verificáveis. | Que toda decisão arquitetural é automaticamente correta. |
| Defesa em profundidade | Ferramentas com mecanismos distintos cobrem riscos distintos e podem se antecipar umas às outras. | Que uma ferramenta substitui a outra. |
| Evidência auditável | PRs, logs, JUnit, cobertura e SBOM tornam a execução rastreável. | Que o artefato por si só prova qualidade do produto. |

## Controles de código e desenho

| Conceito e ferramenta | Na engenharia de software | Aplicação em engenharia de dados | Limite relevante |
| --- | --- | --- | --- |
| Formatação e lint — **Ruff** | Padroniza a forma do código e encontra erros estáticos simples, como nome inexistente, import não usado e construção suspeita. | Evita que um ETL chegue ao runtime com erro Python independente do volume ou da origem dos dados; reduz tempo desperdiçado ao iniciar Spark ou serviços. | Não conhece schema dinâmico de DataFrame nem prova lógica de transformação. |
| Tipagem estática — **mypy** | Verifica compatibilidade entre contratos de funções, argumentos, retornos e atributos antes da execução. | Protege fronteiras tipáveis da orquestração, por exemplo caminho, porta, cliente, configuração e adaptador de persistência. | Não deve ser apresentado como validador de colunas ou tipos dinâmicos do Spark/pandas. |
| Documentação executável — **pydocstringformatter** | Mantém docstrings previsíveis e revisáveis junto do código. | Ajuda a explicitar entrada, saída, efeito externo e exceção de etapas de ingestão, transformação e publicação. | Formato uniforme não torna a descrição verdadeira nem testa comportamento. |
| Complexidade ciclomática — **Radon** | Conta caminhos linearmente independentes de uma função; muitos ramos elevam custo de teste e manutenção. | Sinaliza orquestrações com muitos `if`, tratamento de exceção e decisões de fluxo, que são difíceis de exercitar em reexecuções e falhas operacionais. | É indicador de risco, não defeito funcional; no experimento, o relatório sem bloqueio revelou um falso negativo de configuração. |
| Código morto — **Vulture** | Aponta funções e caminhos possivelmente abandonados. | Reduz manutenção de rotas obsoletas de carga, conectores ou inicialização que podem confundir a operação. | Código invocado dinamicamente pode parecer morto; o limiar de confiança define sensibilidade. |
| Fronteiras arquiteturais — **import-linter** | Impede dependências contrárias à arquitetura declarada. | Evita, por exemplo, que adaptador de S3/PostgreSQL passe a depender da orquestração do pipeline, preservando testabilidade e substituição de infraestrutura. | Só verifica contratos explicitamente escritos. |

## Estratégia de testes

| Conceito e ferramenta | Na engenharia de software | Aplicação em engenharia de dados | Limite relevante |
| --- | --- | --- | --- |
| Teste unitário — **pytest** | Exercita unidade isolada, com falha localizada e feedback rápido. | Testa normalização, decisão de orquestração, montagem de parâmetros e chamadas esperadas sem exigir serviço real. | Mock ou isolamento não prova compatibilidade com PostgreSQL, MinIO ou Spark. |
| Teste baseado em propriedade — **Hypothesis + pytest** | Gera muitos exemplos para verificar invariantes, em vez de depender só de exemplos manuais. | Verifica propriedades técnicas como remover espaços externos de uma chave, para entradas variadas e casos de borda. | Entradas geradas não representam distribuição, qualidade ou semântica do dado de produção. |
| Cobertura — **pytest-cov** | Mede trechos executados pelos testes e pode impor um piso de exercitação. | Dá visibilidade a ramos de orquestração e adaptadores que ficaram sem teste; apoia decisão de onde aprofundar a suíte. | Cobertura não demonstra ausência de defeitos; cobertura agregada de integração pode mascarar queda na cobertura unitária, como ocorreu na v2. |
| Teste de contrato e integração — **pytest, Docker Compose, PostgreSQL, MinIO e Spark** | Verifica interação real entre componentes, protocolo, configuração e efeito externo. | Confirma escrita/leitura JDBC, bucket e objeto, schema técnico, disponibilidade de serviço e publicação do resultado. | Confirma contrato técnico, não validade analítica ou qualidade do conteúdo das linhas. |
| Bootstrap e reexecução | Verifica criação inicial e repetição segura de recursos. | Garante que bucket, tabela ou estrutura necessária possa ser criada e usada novamente sem falhar por estado prévio. | Idempotência técnica não é regra de negócio nem validação de dados. |

## Segurança, dependências e infraestrutura de entrega

| Conceito e ferramenta | Na engenharia de software | Aplicação em engenharia de dados | Limite relevante |
| --- | --- | --- | --- |
| Segurança de código — **Bandit** | Busca padrões inseguros conhecidos em Python, como `shell=True`. | Reduz risco em auxiliares que chamam processos, manipulam credenciais ou constroem comandos de operação do pipeline. | É análise heurística; não prova ausência de vulnerabilidades nem substitui revisão. |
| Auditoria de dependências — **pip-audit** | Consulta vulnerabilidades conhecidas nas bibliotecas resolvidas. | Protege bibliotecas de execução e conectores que processam ou transportam dados. | Depende da base de vulnerabilidades e pode falhar por condição externa, separada da mutação experimental. |
| Segredos versionados — **Gitleaks** | Procura assinaturas de credenciais no repositório. | Evita expor tokens de banco, objeto, API ou CI em código e configuração de pipeline. | Assinaturas não reconhecem todo segredo possível; a V2-GOV-002 documentou uma falsa negativa. |
| Configuração da automação — **Actionlint** | Valida sintaxe e semântica de workflows GitHub Actions. | Garante que a própria esteira que protege o pipeline é executável e que condições, passos e expressões não ficaram inválidos. | Workflow válido não garante que a política de CI seja suficiente. |
| Higiene de imagem — **Hadolint** | Detecta práticas frágeis em Dockerfiles e camadas de imagem. | Ajuda a criar runtimes reprodutíveis para Python/Spark e reduz resíduos de instalação em imagens que executam ETLs. | Não é scanner de vulnerabilidade de imagem nem valida runtime. |
| SQL estático e estrutura dbt — **SQLFluff, dbt parse, compile e build** | Avaliam estilo SQL, grafo de referências e compilação do projeto. | Impedem que modelo, referência ou macro quebre a automação de transformação antes do agendamento. | A estrutura compilar não prova correção analítica, granularidade ou conteúdo do modelo. |

## Governança e rastreabilidade

| Conceito e ferramenta | Papel | Valor para a engenharia de dados |
| --- | --- | --- |
| **pre-commit** | Executa checks mínimos antes do commit. | Reduz feedback tardio e torna a contribuição local mais próxima do ambiente remoto. |
| Lockfile e `uv --frozen` | Fixa a resolução de dependências. | Evita que o mesmo ETL passe em uma máquina e falhe em outra por biblioteca diferente. |
| Relatórios **JUnit** e cobertura | Estruturam resultado de testes para consumo da CI. | Dão rastreabilidade de quais testes executaram e de que código foi exercitado. |
| **SBOM CycloneDX** | Inventaria componentes de software e dependências. | Apoia auditoria e resposta a vulnerabilidades nos ambientes que rodam o pipeline. |
| PR, proteção de branch e logs do GitHub Actions | Preservam revisão, status e evidência do processo. | Impedem integrar mudança sem controles e permitem reconstruir a causa de uma falha experimental. |

## Como apresentar ao orientador

1. Começar pelo problema: pipelines falham não só por dados ruins, mas também
   por código, dependência, configuração, infraestrutura e integração técnica.
2. Explicar que a v2 reutiliza controles consolidados de engenharia de software
   e os posiciona nas fronteiras específicas de um pipeline.
3. Para cada técnica, apresentar **risco → mecanismo de detecção → evidência
   experimental → limite**. O catálogo e o CSV fornecem os dois itens centrais
   de evidência.
4. Não vender os resultados como cobertura total: destacar as seis falsas
   negativas, os dois efeitos externos e as detecções precedentes como parte da
   validade metodológica.
5. Encerrar com a tese defensável: CI eleva a confiabilidade técnica e a
   rastreabilidade da entrega de dados; ela complementa, mas não substitui,
   controles de qualidade dos dados.
