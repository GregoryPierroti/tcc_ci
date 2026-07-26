# Como o experimento é executado

1. Construir o pipeline em Python, PySpark e dbt/SQL.
2. Configurar checks locais reproduzíveis e CI.
3. Injetar uma falha conhecida por branch experimental.
4. Validar localmente e observar a execução remota.
5. Registrar detector, duração e resultado; integrar somente documentação.

Cada falha parte de `baseline-ci-v1`. O protocolo é [[../docs/protocolo-execucao-falhas|documentado]], a cronologia está no [[../docs/registro-metodologico|registro]] e o inventário em [[../fault-catalog/falhas.yml|falhas.yml]].
