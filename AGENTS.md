# Contrato operacional do projeto

Este repositório é o ambiente experimental do TCC sobre a aplicação de uma
esteira convencional de integração contínua a projetos de engenharia de dados.

## Autonomia operacional

O mantenedor autoriza o agente a, dentro deste repositório e do escopo do TCC:

- editar arquivos versionados;
- criar branches, commits e pull requests;
- publicar branches e integrar pull requests limpos em `main`;
- executar Docker Compose, Make, `uv`, dbt, testes e ferramentas de qualidade;
- instalar dependências necessárias às etapas aprovadas do experimento;
- criar documentação, scripts e configurações de CI quando a fase atual os
  solicitar.

As limitações técnicas do ambiente de execução podem ainda solicitar uma
aprovação pontual. Essa solicitação é infraestrutura, e não falta de
autorização funcional do mantenedor.

## Continuidade de rodadas autorizadas

Quando o mantenedor autorizar uma rodada inteira de uma tecnologia ou catálogo
de falhas, o agente deve executá-la até o encerramento: criar e validar cada
experimento, observar a CI remota, registrar os resultados, integrar somente a
documentação e encerrar os ramos defeituosos. Atualizações de progresso não
são um ponto de parada; só devolver o controle ao mantenedor ao concluir a
rodada ou diante de bloqueio real que exija direção, autorização adicional ou
alteração de escopo.

## Rastreabilidade metodológica

- Registrar toda decisão, alteração relevante, validação, falha encontrada e
  integração em `obsidian/50 - Storytelling/Registro metodológico.md`.
- Cada branch e pull request deve ter um objetivo único e verificável.
- Atualizar a documentação antes de integrar uma mudança relevante.
- Registrar comandos executados, resultados observados e limitações que
  afetem a interpretação experimental.

## Convenções Git

- `feat/...`: funcionalidade ou etapa experimental nova.
- `fix/...`: correção de defeito identificado.
- `docs/...`: documentação, protocolo ou organização do fluxo (legado; novas
  notas e especificações ficam em `obsidian/`).
- Preferir um commit coeso por objetivo e uma branch por pull request.
- Antes de commit, executar as validações pertinentes e `git diff --check`.
- Antes de merge, confirmar que o pull request está limpo e mesclável.

## Encerramento de tópicos

Ao concluir um tópico coeso e verificável — por exemplo, uma camada de checks,
uma suíte de testes, uma baseline ou uma rodada de falhas — o agente deve:

1. executar as validações pertinentes e `git diff --check`;
2. registrar a decisão, as evidências e as limitações no diário metodológico;
3. criar um commit coeso que contenha somente os arquivos daquele tópico;
4. informar o hash e aguardar a próxima direção do mantenedor.

Mudanças preexistentes ou fora do tópico nunca devem ser incluídas
automaticamente no commit.

## Segurança e limites

- Não adicionar automaticamente arquivos não rastreados, anexos pessoais,
  dados sensíveis, credenciais ou arquivos `.env`.
- Não apagar arquivos materiais, reescrever histórico ou executar comandos
  destrutivos sem necessidade inequívoca e registro da ação.
- Solicitar direção do mantenedor para: segredos, custos externos,
  infraestrutura fora do escopo local, mudança de objetivo acadêmico ou
  alteração de regra de negócio sem justificativa explícita.
- Não transformar o experimento em uma plataforma genérica de CI.

## Ordem experimental atual

1. Preservar como evidência histórica a rodada v1 (`baseline-ci-v1` e 15
   execuções), sem reescrever seus resultados.
2. Especificar a rodada v2, limitada a práticas de engenharia de software
   aplicadas a pipelines: análise estática, segurança, testabilidade,
   integração técnica e reprodutibilidade.
3. Implementar e validar localmente os checks aprovados para v2.
4. Criar uma nova linha de base saudável (`baseline-ci-v2`) e um catálogo de
   falhas próprio; não reutilizar a tag ou o catálogo executado da v1.
5. Executar as mutações v2 de forma controlada e consolidar a comparação entre
   as rodadas.

## Delimitação da rodada v2

- A v2 não avalia *data quality*, como completude, nulidade, unicidade ou
  cardinalidade do conteúdo produzido.
- Testes de contrato e integração podem verificar interfaces técnicas entre
  componentes — arquivo, schema técnico, tabela, conexão, bootstrap e
  reexecução — sem alegações sobre qualidade dos dados.
- A ampliação permanece limitada às técnicas documentadas no
  `obsidian/10 - Especificação/Plano da rodada v2.md`; não transformar o
  experimento em uma plataforma genérica de CI.
