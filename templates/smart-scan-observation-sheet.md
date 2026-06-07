# Fiche observation Smart Scan

| Champ | Valeur |
|---|---|
| Responsable |  |
| Date |  |
| Environnement |  |
| Version Exadata / GI / DB |  |
| Périmètre |  |
| Hypothèses |  |
| Risques connus |  |
| Validation requise |  |

## Collecte read-only

```bash
hostname -f
date
crsctl stat res -t
srvctl status database -v
asmcmd lsdg
cellcli -e list cell detail
```

## Analyse

| Point contrôlé | Observation | Risque | Action proposée | Propriétaire |
|---|---|---|---|---|
|  |  |  |  |  |

## Décision

La décision doit être validée par les responsables DBA, infrastructure et métier lorsque le changement touche production, disponibilité, performance, sécurité ou support.
