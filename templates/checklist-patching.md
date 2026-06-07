# Checklist Patching

## Usage

Ce modèle est directement exploitable dans le cours V3. Il doit être rempli avec des preuves réelles de l’environnement et ne doit pas contenir de secrets, mots de passe, clés privées, chaînes de connexion ou données client non anonymisées.

## Contexte

| Champ | Valeur |
|---|---|
| Environnement | |
| Type Exadata | On-prem / Exadata Database Service / Cloud@Customer |
| Date et heure | |
| Responsable | |
| Périmètre | |
| Incident / changement / audit | |

## Collecte read-only recommandée

| Couche | Commande ou preuve | Résultat attendu | Commentaire |
|---|---|---|---|
| DB / GI | `crsctl stat res -t` ou vue SQL adaptée | État cluster et services | Adapter aux privilèges. |
| ASM / storage | `asmcmd lsdg` ou `cellcli list ...` | Capacité, état, alertes | Ne pas exécuter d’action offline/drop. |
| Support | `tfactl print status`, `exachk -v` | État outils support | Collecte complète seulement si autorisée. |

## Analyse

| Point de contrôle | Conforme | Preuve | Risque | Action recommandée |
|---|---|---|---|---|
| | | | | |
| | | | | |

## Décision

| Décision | Critère | Responsable | Date |
|---|---|---|---|
| Go / No-Go / À revoir | | | |

## Notes de sécurité

Toute commande de modification, redémarrage, patching, suppression, mise hors ligne, changement réseau ou changement de paramètre doit être déplacée dans un runbook approuvé. Ce modèle est conçu pour documenter, comparer et décider, pas pour modifier l’environnement.
