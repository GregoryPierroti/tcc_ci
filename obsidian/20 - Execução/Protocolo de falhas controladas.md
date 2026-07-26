# Protocolo de falhas controladas

## Regras invariáveis

- Uma única mutação, em uma branch `fault/<id>`, criada da tag basal.
- A PR experimental é observada, mas nunca integrada.
- O resultado documental é integrado somente após evidência local e remota.
- A classificação usa `detected`, `false_negative`, `false_positive` ou
  `inconclusive`.

## Fluxo

1. Selecionar uma falha ainda não executada no catálogo.
2. Criar a branch da tag `baseline-ci-v1`, aplicar a mutação e validar localmente.
3. Abrir PR experimental e observar o primeiro check remoto bloqueante.
4. Registrar commit, detector esperado/observado, duração, URL e classificação.
5. Se a CI passar, executar o oráculo integral indicado; confirmar ou descartar
   falso negativo.
6. Atualizar registro metodológico e CSV; fechar PR e remover branch defeituosa.

O texto completo e normativo permanece em [[../../docs/protocolo-execucao-falhas|docs/protocolo-execucao-falhas]].

Veja [[Estado e próximos passos]] e [[../40 - Evidências/Resultados e métricas]].
