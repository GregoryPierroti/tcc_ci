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

## Rastreabilidade metodológica

- Registrar toda decisão, alteração relevante, validação, falha encontrada e
  integração em `docs/registro-metodologico.md`.
- Cada branch e pull request deve ter um objetivo único e verificável.
- Atualizar a documentação antes de integrar uma mudança relevante.
- Registrar comandos executados, resultados observados e limitações que
  afetem a interpretação experimental.

## Convenções Git

- `feat/...`: funcionalidade ou etapa experimental nova.
- `fix/...`: correção de defeito identificado.
- `docs/...`: documentação, protocolo ou organização do fluxo.
- Preferir um commit coeso por objetivo e uma branch por pull request.
- Antes de commit, executar as validações pertinentes e `git diff --check`.
- Antes de merge, confirmar que o pull request está limpo e mesclável.

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

1. Recuperar e validar localmente os objetos experimentais.
2. Consolidar qualidade e testes locais reproduzíveis.
3. Implementar CI por projeto, começando pelo ETL Python.
4. Catalogar e injetar falhas de forma controlada.
5. Consolidar métricas e resultados para a monografia.
