# Desenho metodológico

1. Preservar a v1 como linha de base e resultado histórico.
2. Configurar, para a v2, checks locais e remotos adequados a cada tecnologia.
3. Validar a esteira saudável e criar uma tag de referência exclusiva da v2.
4. Injetar uma falha conhecida por vez, em branch experimental isolada.
5. Observar o primeiro detector causal na CI e executar confirmação técnica
   independente quando a hipótese não for bloqueada pelo controle avaliado.
6. Registrar resultado, duração, limitações e comparar tecnologias e rodadas.

## Unidades de análise e fontes

| Unidade | Identificador e fonte | Uso metodológico |
| --- | --- | --- |
| Execução | uma linha `execution_id` em [[../../results/resultados.csv\|resultados.csv]] | Registra uma tentativa concreta: baseline, commit, detectores esperado e observado, duração, desfecho e URL do job. |
| Mutação única | um `fault_id` nos [[../../fault-catalog/falhas.yml\|catálogo v1]] ou [[../../fault-catalog/falhas-v2.yml\|catálogo v2]] | Representa a hipótese técnica controlada. Pode possuir mais de uma execução quando houver repetição metodológica. |
| Detector-alvo | `expected_detector` e `expected_stage` do catálogo | Expressa a hipótese operacional original. Não deve ser reescrito para coincidir com o primeiro detector observado. |
| Detector observado | `observed_detector` e `observed_stage` do CSV | Registra o primeiro bloqueio efetivamente observado, ou sua ausência quando a CI aprova a execução. |

Execução e mutação não são sinônimos. A v1 possui 15 execuções registradas
para 15 mutações; a v2 possui 33 execuções para 28 mutações únicas porque cinco
hipóteses exigiram repetição. Portanto, totais e percentuais devem declarar
explicitamente se o denominador é **execução** ou **mutação única**. Essas
proporções descrevem o catálogo observado e não estimam cobertura geral de
defeitos.

## Classificação da evidência observada

| Classificação | Definição operacional | Consequência para a análise |
| --- | --- | --- |
| Detecção causal | O primeiro bloqueio é diretamente provocado pela mutação, conforme diagnóstico do job e confirmação técnica disponível. | O detector observado pode sustentar a interceptação da mutação. |
| Detecção causal precedente | Um controle anterior ou diferente bloqueia a mesma causa antes do detector-alvo. | Demonstra defesa em profundidade, mas não confirma o detector originalmente esperado; a hipótese pode exigir repetição isolada. |
| Repetição metodológica | Nova execução do mesmo `fault_id` para remover um confundidor, isolar a hipótese ou revalidar a baseline. | É uma propriedade do protocolo, não um novo defeito nem um desfecho alternativo. A primeira execução permanece no CSV. |
| Falso negativo | A falha técnica é confirmada de forma independente, mas o controle avaliado não a bloqueia. | Expõe limite de configuração, limiar, composição de checks ou cenário não exercitado; não prova ausência de defeitos no sistema. |
| Falso positivo externo | O workflow falha por causa real, porém independente da mutação controlada. | Deve ser separado da eficácia do detector-alvo. Não implica que a ferramenta que encontrou a causa externa esteja errada. |

Efeitos posteriores à interrupção — por exemplo, upload de JUnit ou SBOM sem
artefato após um check bloqueante — não são detectores causais nem falsos
positivos externos. Eles são registrados como efeitos secundários nos campos de
notas e não recebem crédito de detecção.

## Procedimento de leitura

1. Consultar o catálogo da rodada para recuperar mutação, técnica, detector e
   etapa esperados.
2. Localizar no CSV a execução pelo `execution_id` ou pelo `fault_id`,
   preservando o `baseline_tag` efetivamente registrado.
3. Conferir a URL em `evidence_url`, o commit da mutação e as notas para
   identificar o primeiro detector causal, uma causa externa ou um efeito
   secundário.
4. Usar o [[../50 - Storytelling/Registro metodológico|registro metodológico]]
   para recuperar confirmação independente, revalidação de baseline e motivo
   de eventual repetição.
5. Classificar a evidência sem alterar retrospectivamente a hipótese do
   catálogo; a matriz comparativa deve mostrar esperado e observado em colunas
   distintas.

## Controles de validade e delimitação

- Cada rodada possui tag, catálogo e resultados próprios. A v1 usa
  `baseline-ci-v1`; a v2 inicia em `baseline-ci-v2` e preserva no CSV as
  referências reconstruídas usadas após a revalidação de segurança.
- Código defeituoso nunca é integrado ao `main`.
- Resultado esperado (catálogo) e resultado observado (CSV) são separados.
- Falsos negativos da v2 são confirmados por teste técnico independente de
  integração, contrato, bootstrap, cobertura ou reexecução, não por *data
  quality*.
- Cada falha v2 declara a técnica de engenharia avaliada, detector esperado e
  limite interpretativo.
- O escopo avalia engenharia de software aplicada a pipelines: código,
  configuração, dependências, automação, imagem e interfaces técnicas. Não
  avalia nulidade, completude, unicidade, cardinalidade ou correção do conteúdo
  processado. CI pode complementar controles de qualidade de dados, mas não os
  substitui.

O procedimento executável está no [[../20 - Execução/Protocolo de falhas controladas|protocolo de falhas controladas]].
O escopo está no [[Plano da rodada v2|plano da v2]].
