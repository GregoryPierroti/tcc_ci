# Estado e próximos passos

> [!important] Ponto de handoff — 2026-07-26
> Antes de retomar experimentos, a próxima sessão deve revalidar a organização
> do vault Obsidian. A organização documental é a prioridade imediata; a rodada
> dbt permanece pausada até essa validação.

## Estado consolidado

| Frente | Situação | Evidência de entrada |
| --- | --- | --- |
| Linha de base e CI | concluídas para Python, PySpark e dbt | [[../10 - Especificação/Linha de base experimental]] |
| Rodada Python | concluída: 5 detecções | [[../40 - Evidências/Resultados e métricas]] |
| Rodada PySpark | concluída: 3 detecções e 2 falsos negativos | [[../40 - Evidências/Resultados e métricas]] |
| Rodada dbt | pausada; catálogo preparado | [[../40 - Evidências/Catálogo de falhas]] |
| Obsidian | migrado e reorganizado; requer revisão de navegação | [[../00 - Início/00 - Dashboard]] |

## Pendência experimental preservada

A PR experimental **#30 / DBT-001** permanece aberta na branch `fault/DBT-001`
e não foi integrada ao `main`. A CI remota falhou em **57 s** no job
`SQLFluff, parse, compile e dbt build`; localmente, o lint falhou enquanto
`dbt parse` e `dbt compile` passaram. O resultado ainda **não** foi registrado
no CSV nem no diário, portanto a próxima sessão deve primeiro decidir se a
mutação/catálogo será mantida como evidência válida ou ajustada.

## Próxima sessão: revalidar o vault

1. Abrir `obsidian/` como vault e iniciar em [[../00 - Início/00 - Dashboard]].
2. Percorrer o fluxo: dashboard → índice mestre → visão/problema → desenho →
   tecnologias → evidências → storytelling.
3. Confirmar que cada assunto tem **uma única nota canônica** e que não há
   conteúdo de especificação fora de `obsidian/`.
4. Verificar se os links para código, catálogo YAML e CSV ajudam a recuperar a
   evidência sem criar uma segunda especificação.
5. Avaliar se os nomes, a granularidade e a ordem servem simultaneamente para
   leitura humana, redação da monografia e contexto de IA.
6. Registrar qualquer ajuste estrutural no [[../50 - Storytelling/Registro metodológico]].

## Após a validação documental

1. Fechar ou registrar DBT-001 conforme a evidência já observada.
2. Executar DBT-002 a DBT-005 pelo [[Protocolo de falhas controladas]].
3. Consolidar a matriz final de detecção, duração, adaptação e falsos negativos.

## Fora de escopo até então

Mypy, artefatos de cobertura/JUnit, auditoria de dependências dbt e testes
unitários nativos dbt continuam como melhorias posteriores. Eles não bloqueiam
a revisão do vault nem a rodada atual de falhas.
