# Interpretação comparativa v1–v2

## O que a comparação sustenta

As duas rodadas demonstram que práticas de integração contínua podem ser
adaptadas a pipelines como controles de engenharia de software: análise
estática, tipagem, testes unitários e de integração, resolução de dependências,
fronteiras arquiteturais, automação de workflows, higiene de imagens e
segurança de código. A v1 constitui a linha de base histórica com 15 execuções;
a v2 amplia o conjunto técnico para 33 execuções e 28 mutações únicas. Os
totais e a matriz de evidências estão em
[[Resultados e métricas|resultados e métricas]] e na
[[Matriz comparativa final|matriz comparativa]].

Essa ampliação não autoriza interpretar 13/15 (86,7%) na v1 e 25/33 (75,8%) na
v2 como variação de eficácia entre rodadas. Ambos são percentuais de
**execuções**, os catálogos diferem e a v2 contém cinco repetições. A comparação
é, portanto, de desenho, diversidade de controles e limites empíricos — não de
cobertura geral de defeitos.

## Detecção direta, precedente e isolamento da hipótese

Em diversas execuções, detector esperado e observado coincidiram: Ruff, mypy
na repetição V2-PY-003, import-linter, pytest em contratos técnicos, SQLFluff,
Bandit B602, Actionlint e Hadolint bloquearam diretamente mutações do catálogo.
Isso sustenta a utilidade desses checks para os riscos especificamente
injetados.

Outras linhas mostram defesa em profundidade, mas exigem atribuição cuidadosa.
Ruff F401 antecipou mypy em V2-PY-003; Ruff format antecipou a integração em
V2-SP-007; o teste unitário de orquestração antecipou a integração em
V2-SP-008; e SQLFluff com templater dbt antecipou `dbt parse` em V2-DBT-002.
Esses são casos de detecção causal precedente, não confirmação automática do
detector inicialmente previsto. As repetições V2-PY-003 e V2-SP-007 removem o
confundidor e confirmam o detector-alvo; V2-SP-008 permanece precedente porque
o primeiro bloqueio técnico já interceptou a mesma causa.

V2-GOV-001 é diferente: Bandit B602 é a detecção causal direta, embora a
denominação da etapa observada seja mais curta que a etapa esperada. Em
V2-SP-004, a suíte pytest é causal, mas a evidência não permite atribuir a
detecção exclusivamente ao Hypothesis, pois o teste determinístico também
cobre a mutação. Na v1, DBT-001 também requer precisão: a retirada da vírgula
formou alias implícito, SQLFluff reportou AL02 e `dbt parse`/`compile`
aprovaram; não se trata simplesmente de SQL inválido.

## Limites configuracionais observados

### Cobertura agregada

V2-PY-010 e V2-SP-005 testaram um piso unitário de 95% das linhas
instrumentadas. As confirmações locais mediram, respectivamente, 94,66% e
94,58% dessas linhas, mas os workflows remotos aprovaram
porque agregaram testes de níveis distintos antes de aplicar a cobertura. O
achado não é que cobertura seja inútil: ele mostra que o gate efetivamente
executado mede a cobertura composta, e não preserva o contrato de cobertura
unitária formulado no catálogo. A correção metodológica é tratar esses dois
casos como falsos negativos e, para um futuro redesenho, separar a geração e a
verificação do artefato de cobertura por escopo de teste.

### Radon e Vulture

Em V2-PY-005, Radon listou complexidade C (14), mas o comando
`radon cc . -n B -s` somente reportou a ocorrência e retornou sucesso. Logo, o
limiar configurado não era um gate bloqueante. Em V2-PY-006, Vulture encontrou
a função sem referência com escore de confiança 60/100 localmente, enquanto a CI exigia
`--min-confidence 100`; o job aprovou de acordo com essa configuração. Os
dois falsos negativos não invalidam as ferramentas: delimitam, respectivamente,
a semântica de saída do comando e o limiar de confiança escolhido. Uma alteração
de configuração deve ser avaliada como nova intervenção, não inferida como
resultado já demonstrado nesta rodada.

### Gitleaks e o controle precedente Bandit

V2-GOV-002 separa dois fatos. Na primeira execução, Bandit B105 bloqueou a
constante sintética antes do Gitleaks: uma detecção causal precedente para a
mesma causa. Ao mover a assinatura para comentário, a repetição removeu esse
confundidor e Gitleaks aprovou; trata-se de falso negativo para aquela assinatura
sintética, não de prova de que todo segredo seria omitido. O limite é coerente
com um detector baseado em assinaturas e não deve ser generalizado além da
mutação avaliada.

### Reexecução e idempotência técnica

Em V2-PY-014, a confirmação independente demonstrou falha na segunda chamada
de `ensure_base_structure`, mas a suíte remota aprovou a repetição causal. A
primeira tentativa foi interrompida por `PYSEC-2026-3721` em `pip 26.1.2`; esse
achado era real, porém externo à mutação. Após a revalidação em baseline
reconstruída, a aprovação da CI confirmou que a suíte não exercita reexecução.
O resultado é um falso negativo do controle de integração para idempotência
técnica, não um falso alarme do pip-audit.

## Implicações para o desenho de CI

Os resultados favorecem uma esteira em camadas: controles rápidos de formato,
lint, tipo e arquitetura interceptam riscos de código antes do runtime; testes
unitários e de integração verificam contratos técnicos de adaptadores,
bootstrap e publicação; e controles de governança verificam automação, imagem
e segurança. Detectores precedentes reduzem o tempo até o primeiro bloqueio,
mas também tornam indispensável registrar o detector-alvo separadamente do
observado.

A validade desse desenho depende de três cuidados: manter a baseline real de
cada execução no CSV, preservar a primeira tentativa quando houver repetição e
confirmar independentemente todo aprovado que possa esconder a falha técnica.
Os dois falsos positivos externos ilustram por que uma falha de workflow não
deve ser atribuída automaticamente à mutação; os efeitos posteriores, como
uploads sem artefato, tampouco são detectores.

## Delimitação

Esta análise não mede nulidade, completude, unicidade, cardinalidade ou
correção do conteúdo processado. Ela avalia a engenharia de software que torna
pipelines mais verificáveis e reproduzíveis; CI pode complementar, mas não
substitui, controles de *data quality*. As conclusões restringem-se às mutações
controladas, às baselines registradas e aos jobs documentados no
[[../../results/resultados.csv|CSV]].

Para recuperar a evidência de cada afirmação, use a
[[Rastreabilidade das evidências|cadeia catálogo → CSV → job/PR → diário]].
