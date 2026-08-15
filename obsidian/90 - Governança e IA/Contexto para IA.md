# Contexto para IA

> [!important] Leitura correta
> Este vault é mapa semântico; arquivos versionados são a fonte de verdade. Check aprovado não implica ausência de defeitos.

## Vocabulário

- **baseline:** estado reprodutível de uma rodada; a v1 usa `baseline-ci-v1`
  e a v2 só terá tag após a validação da esteira ampliada.
- **falha controlada:** mutação intencional, isolada e não integrável.
- **detector:** primeiro check que bloqueou uma falha.
- **falso negativo:** CI aprovada apesar de efeito revelado por validação externa.
- **teste técnico independente:** confirma defeito de contrato, integração,
  bootstrap ou reexecução quando a CI aprova uma mutação.
- **data quality:** propriedades do conteúdo, como completude, nulidade,
  unicidade e cardinalidade; está fora do escopo da v2.

## Ordem recomendada

Leia [[../00 - Início/00 - Dashboard|o painel inicial]],
[[../10 - Especificação/Visão e problema de pesquisa|a pergunta de pesquisa]],
[[../10 - Especificação/Desenho metodológico|o desenho metodológico]],
[[../30 - Tecnologias/Mapa de tecnologias e checks|o mapa de checks]] e
[[../40 - Evidências/Resultados e métricas|o resumo de resultados]]. Abra catálogo, CSV e diário para
números, decisões e resultados específicos. Diferencie sempre evidência v1,
planejamento v2 e resultado v2 observado.

Ao responder, diferencie esperado de observado, cite tecnologia, baseline e
identificador de falha. A rodada dbt da v1 está consolidada; não a trate como
resultado da v2.
