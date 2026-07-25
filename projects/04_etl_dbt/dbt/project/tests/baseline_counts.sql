with expected as (
    select 'mod_bancos' as relation_name, 1474::bigint as expected_count
    union all select 'mod_reclamacoes', 918::bigint
    union all select 'mod_empregados', 39::bigint
    union all select 'mod_final', 1::bigint
),
actual as (
    select 'mod_bancos' as relation_name, count(*)::bigint as actual_count from {{ ref('mod_bancos') }}
    union all select 'mod_reclamacoes', count(*)::bigint from {{ ref('mod_reclamacoes') }}
    union all select 'mod_empregados', count(*)::bigint from {{ ref('mod_empregados') }}
    union all select 'mod_final', count(*)::bigint from {{ ref('mod_final') }}
)

select
    expected.relation_name,
    expected.expected_count,
    actual.actual_count
from expected
join actual using (relation_name)
where expected.expected_count <> actual.actual_count
