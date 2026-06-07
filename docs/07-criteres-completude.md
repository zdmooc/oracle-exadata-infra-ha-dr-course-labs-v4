# Critères de complétude du cours Exadata

Un module est considéré complet lorsqu’il contient objectifs, concepts, architecture, explications, commandes de lecture non destructives, points de vigilance, erreurs fréquentes, bonnes pratiques, mini-lab, questions de validation, livrables attendus et références officielles.

| Critère | Statut attendu | Méthode de vérification |
|---|---|---|
| Couverture syllabus | Les thèmes Oracle University publics sont mappés vers les modules. | Lire `docs/04-mapping-syllabus-oracle-university.md`. |
| Modules 00 à 27 | Tous les fichiers existent et suivent une structure homogène. | Vérifier `modules/`. |
| Labs complets | Chaque lab contient objectif, prérequis, contexte, commandes, résultat, validation, nettoyage, risques et livrable. | Vérifier `labs/`. |
| Sécurité | Les commandes destructives sont absentes ou marquées comme risquées. | Rechercher les verbes `drop`, `delete`, `modify`, `patch`, `restart`. |
| Références | Les documents pointent vers Oracle University et Oracle Docs. | Vérifier les liens de références. |
| Plus du dépôt existant | Architecture, site planning, OEDA/OECA, storage/ASM, IORM, HA/DR, patching, Cloud@Customer et troubleshooting conservés. | Comparer README, modules et templates. |

## Références officielles

[1]: https://education.oracle.com/exadata-database-machine-administration-workshop/courP_4599 "Oracle University — Exadata Database Machine Administration Workshop"
[2]: https://docs.oracle.com/en/engineered-systems/exadata-database-machine/ "Oracle Exadata Database Machine Documentation"
[3]: https://docs.oracle.com/en/engineered-systems/exadata-database-machine/sagug/ "Oracle Exadata System Software User's Guide"
[4]: https://docs.oracle.com/en/engineered-systems/exadata-database-machine/dbmmn/ "Oracle Exadata Database Machine Maintenance Guide"
[5]: https://docs.oracle.com/en/database/oracle/oracle-database/ "Oracle Database Documentation"
[6]: https://www.oracle.com/database/maximum-availability-architecture/ "Oracle Maximum Availability Architecture"
[7]: https://docs.oracle.com/en/cloud/paas/exadata-cloud/ "Oracle Exadata Cloud Service Documentation"
[8]: https://docs.oracle.com/en/cloud/cloud-at-customer/exadata-cloud-at-customer/ "Oracle Exadata Cloud@Customer Documentation"
