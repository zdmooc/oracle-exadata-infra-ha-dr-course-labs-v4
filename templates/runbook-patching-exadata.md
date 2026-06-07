# Runbook patching Exadata

## Objectif

Ce runbook structure un patching Exadata en distinguant les couches **Oracle Database**, **Grid Infrastructure**, **OS DB servers**, **Exadata System Software storage cells**, **outils support** et **monitoring**. Il ne remplace pas les notes Oracle applicables ni les procédures internes CAB.

## Périmètre et responsabilités

| Domaine | Responsable | Preuve attendue | Statut |
|---|---|---|---|
| Sauvegarde/recoverability | DBA | `list backup summary`, restore test ou validation documentée | |
| Data Guard / DR | DBA HA | `show configuration`, lag, rôle primaire/standby | |
| Cluster / GI | DBA/GI | `crsctl stat res -t`, `srvctl status database` | |
| Storage cells | Admin Exadata | `cellcli list cell detail`, alerthistory | |
| Monitoring | NOC/DBA | Blackouts EM, alerting post-patch | |
| Support Oracle | Owner SR | Notes patch, SR préventif si nécessaire | |

## Pré-check read-only

```bash
imageinfo
imagehistory
opatch lsinventory
crsctl stat res -t
srvctl status database -d <db_unique_name> -v
cellcli -e "list alerthistory where severity != clear detail"
exachk
```

## Go / No-Go

| Critère | Go si | No-Go si |
|---|---|---|
| Backup | Sauvegarde récente et recoverability validée | Backup absent, FRA critique, restore jamais testé |
| HA/DR | Data Guard sain ou risque accepté | Lag non expliqué, standby indisponible sans acceptation |
| Santé plateforme | Alertes connues et documentées | Alerte critique non résolue |
| Fenêtre | Communication et rollback prêts | Fenêtre insuffisante ou sponsor indisponible |

## Exécution

L’exécution réelle doit suivre la note Oracle du patch concerné. Toute commande de patching est volontairement exclue de ce modèle de cours et doit être insérée uniquement par l’équipe autorisée après validation.

## Post-check

```bash
imageinfo
opatch lsinventory
crsctl stat res -t
srvctl status service -d <db_unique_name>
cellcli -e "list alerthistory where severity != clear detail"
exachk
```

## Rollback et escalade

Documenter le point de décision, la méthode de retour arrière prévue par la note Oracle, les logs à collecter, le SR Oracle éventuel et la communication métier.
