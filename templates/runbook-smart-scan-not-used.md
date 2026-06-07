# Runbook Smart Scan non utilisé

## Collecte SQL

```sql
select * from table(dbms_xplan.display_cursor('&SQL_ID', null, 'ALLSTATS LAST +IOSTATS +PREDICATE'));
select sql_id,cell_offload_eligible_bytes,cell_offload_returned_bytes,physical_read_bytes from v$sql where sql_id='&SQL_ID';
select name,value from v$sysstat where name like 'cell%';
```

## Diagnostic

| Cause possible | Comment vérifier | Remédiation prudente |
|---|---|---|
| Accès index très sélectif | Plan `INDEX RANGE SCAN` | Pas nécessairement un problème. |
| Pas de direct path/full scan | Plan et statistiques I/O | Tester en environnement non critique. |
| Prédicat non offloadable | Section predicates DBMS_XPLAN | Réécriture SQL seulement après test. |
| Projection colonnes trop large | Colonnes retournées et interconnect bytes | Réduire sélection si métier possible. |
| Stats objets obsolètes | `dba_tab_statistics` | Collecte stats via runbook approuvé. |
