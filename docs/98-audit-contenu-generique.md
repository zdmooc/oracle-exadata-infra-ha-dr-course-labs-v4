# Audit du contenu générique V2 et corrections V3

La V2 contenait une structure solide mais de nombreux modules répétaient des blocs génériques tels que des commandes système élémentaires répétées et des mini-labs trop similaires. La V3 remplace ces répétitions par des commandes, vues, métriques et livrables propres à chaque sujet.

| Problème V2 détecté | Correction V3 |
|---|---|
| Commandes système identiques dans presque tous les modules | Remplacement par commandes CellCLI, ASM, CRS, RMAN, Data Guard, EM, AHF ou OCI selon le module. |
| Mini-labs génériques | Chaque module possède un mini-lab ciblé et chaque lab possède contexte, risques, commandes et livrable. |
| Smart Scan sans métriques d’offload | Ajout `DBMS_XPLAN`, `v$sql`, `v$sysstat`, métriques eligible/returned/storage index. |
| IORM trop conceptuel | Ajout plan IORM, consumer groups, noisy neighbor, matrice workload/priorité. |
| Bulk loading insuffisant | Ajout DBFS, external tables, SQL Loader, Data Pump, direct path, contraintes, rollback. |
| Monitoring non séparé | Modules dédiés software, EM, storage cells, DB servers, réseau, autres composants, outils. |
| Patching trop haut niveau | Ajout pré-check, patchmgr, DB/GI/OS, Data Guard, Exachk, rollback, Go/No-Go. |
| Support ecosystem superficiel | Ajout AHF, TFA, Exachk, ORAchk, ASR, SR, revue sécurité logs. |

Les modules 08, 10, 13, 14 à 21, 22, 23, 25, 26 et 27 ont été renforcés en priorité conformément aux exigences V3.
