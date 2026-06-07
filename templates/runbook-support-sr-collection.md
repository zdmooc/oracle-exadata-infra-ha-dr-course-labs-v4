# Runbook collecte support SR Exadata

## Objectif

Préparer un dossier SR Oracle complet, horodaté et anonymisé, avec impact métier, timeline, preuves techniques et logs nécessaires.

## Informations SR

| Champ | Valeur |
|---|---|
| Impact métier | |
| Heure de début | |
| Composants touchés | DB / ASM / cell / réseau / cloud / autre |
| Changements récents | |
| RPO/RTO ou criticité | |

## Collecte read-only

```bash
ahfctl status
tfactl print status
exachk -v
cellcli -e "list alerthistory detail"
crsctl stat res -t
```

## Collecte ciblée TFA

La collecte `tfactl diagcollect` peut être volumineuse et contenir des informations sensibles. Définir la fenêtre temporelle et relire les fichiers avant upload.

## Revue sécurité

| Élément | Action |
|---|---|
| Mots de passe / tokens | Supprimer ou masquer. |
| Données client | Anonymiser. |
| OCID / IP publiques | Masquer si politique interne l’exige. |
| Logs volumineux | Compresser et référencer proprement. |
