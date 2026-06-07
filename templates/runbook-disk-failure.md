# Runbook suspicion panne disque Exadata

## Collecte read-only

```bash
cellcli -e "list physicaldisk detail"
cellcli -e "list celldisk detail"
cellcli -e "list griddisk attributes name,status,asmmodestatus,asmdeactivationoutcome"
cellcli -e "list alerthistory where alertMessage like '%disk%' detail"
asmcmd lsdsk -k
```

## Points de contrôle

| Objet | Information critique | Commentaire |
|---|---|---|
| Physical disk | État matériel, slot, erreur prédictive | Identifier exactement le composant. |
| Cell disk | Lien logique avec physical disk | Éviter confusion objet. |
| Grid disk | État présenté à ASM | Vérifier `asmdeactivationoutcome`. |
| ASM disk | Failgroup, mount/mode/state | Vérifier résilience. |

## Actions interdites dans le cours

Les opérations de suppression, modification d’état, mise hors ligne, remplacement disque, redémarrage ou resynchronisation forcée sont hors périmètre du lab et doivent être gérées par support ou runbook officiel.
