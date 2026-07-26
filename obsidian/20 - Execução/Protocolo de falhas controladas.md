# Protocolo de execução de falhas controladas

## Objetivo e limite

Este protocolo executa uma única mutação por vez, para medir a capacidade da
CI de detectá-la. A branch de uma falha nunca é integrada ao `main`; o
resultado é registrado separadamente após a observação.

## Preparação

1. Confirmar que `baseline-ci-v1` aponta para o baseline saudável.
2. Escolher uma entrada em `fault-catalog/falhas.yml` ainda não executada.
3. Criar uma branch a partir da tag: `git switch -c fault/<id> baseline-ci-v1`.
4. Aplicar somente a mutação descrita no catálogo e criar um único commit.
5. Abrir uma pull request com o identificador da falha e sem solicitar merge.

## Execução e observação

1. Aguardar a execução do workflow indicado no catálogo.
2. Registrar no CSV o commit, o status do workflow, a primeira etapa que
   falhou e a duração total do job exibida pelo GitHub Actions.
3. Comparar o detector e a etapa observados com os valores esperados.
4. Se a CI passar, executar localmente o comando de integração ou o oráculo
   indicado no catálogo para confirmar que a mutação realmente produziu o
   defeito; registrar o caso como falso negativo se confirmado.
5. Classificar como falso positivo somente se a CI falhar sem relação causal
   com a mutação; registrar a evidência no diário metodológico.

## Encerramento

1. Registrar uma linha em `results/resultados.csv`, sem incluir o código com
   defeito no `main`.
2. Documentar no diário metodológico a falha, a evidência e limitações.
3. Fechar a pull request sem merge e remover a branch remota e local quando
   não forem mais necessárias.
4. Voltar ao baseline com `git switch main` e confirmar a tag antes da próxima
   execução.

## Convenções de resultado

- `detected`: a CI falhou na etapa esperada ou em uma etapa anterior que
  inequivocamente detecta a mesma mutação.
- `false_negative`: a CI passou e o oráculo independente confirmou o defeito.
- `false_positive`: a CI falhou por causa não relacionada à mutação.
- `inconclusive`: não foi possível atribuir o resultado; exige repetição e
  registro da limitação antes de qualquer interpretação quantitativa.
