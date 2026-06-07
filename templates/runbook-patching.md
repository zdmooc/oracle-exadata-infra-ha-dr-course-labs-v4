# Runbook de patching Exadata

| Phase | Action | Responsable | Preuve | Go/No-Go |
|---|---|---|---|---|
| Préparation | Confirmer versions source/cible et documentation Oracle | DBA/Infra | Notes de version |  |
| Pré-check | Exachk, sauvegardes, Data Guard, alertes, capacité | DBA | Rapport |  |
| Communication | Informer métiers, exploitation, support | Change manager | Ticket changement |  |
| Exécution | Suivre la procédure Oracle validée | DBA/Oracle | Journal |  |
| Validation | Services, ASM, cells, performance, alertes | DBA/App | Rapport post-check |  |
| Rollback | Appliquer uniquement si critères définis | DBA/Oracle | Décision formelle |  |
