# Runbook cellule storage suspecte ou indisponible

## Avertissement

Ce runbook est principalement **diagnostic read-only**. Toute action de mise offline, drop, alter, remplacement physique ou redémarrage doit être conduite uniquement avec procédure Oracle/support validée.

## Collecte initiale

```bash
cellcli -e "list cell detail"
cellcli -e "list physicaldisk detail"
cellcli -e "list celldisk detail"
cellcli -e "list griddisk attributes name,status,asmmodestatus,asmdeactivationoutcome"
cellcli -e "list alerthistory detail"
asmcmd lsdg
```

## Analyse

| Question | Preuve | Décision |
|---|---|---|
| La cell répond-elle ? | `list cell detail` | |
| Les griddisks sont-ils utilisables par ASM ? | `asmmodestatus`, `asmdeactivationoutcome` | |
| L’alerte est-elle active ou historique ? | `alerthistory severity` | |
| ASM peut-il tolérer une indisponibilité ? | `usable_file_mb`, redundancy, failgroups | |

## Sortie attendue

Produire un dossier incident avec timestamp, cell concernée, objets impactés, état ASM, alertes et recommandation d’escalade.
