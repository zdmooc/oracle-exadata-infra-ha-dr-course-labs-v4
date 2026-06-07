# Runbook diagnostic latence I/O Exadata

## Objectif

Identifier si une latence observée vient du SQL, de l’ASM, des storage cells, du réseau privé ou d’un workload concurrent.

## Collecte

```sql
select event,total_waits,time_waited from v$system_event where event like 'cell%' order by time_waited desc;
select sql_id,elapsed_time,executions,physical_read_bytes from v$sql order by elapsed_time desc fetch first 20 rows only;
```

```bash
cellcli -e "list metrichistory attributes name,metricObjectName,metricValue where metricObjectType = 'GRIDDISK'"
cellcli -e "list alerthistory where severity != clear detail"
asmcmd lsdg
```

## Corrélation

| Hypothèse | Preuve favorable | Preuve contraire |
|---|---|---|
| SQL inefficace | SQL_ID dominant, plan instable | Plusieurs bases touchées simultanément |
| Cell saturée | Métriques griddisk/flash anormales sur une cell | Toutes les cells stables |
| Réseau privé | erreurs/drops interfaces, RDMA down | Aucun compteur réseau, latence localisée SQL |
| Noisy neighbor | I/O forte autre workload, IORM absent/faible | Charge isolée à un SQL |
