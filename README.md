# Oracle Exadata Database Machine Administration Workshop — Cours complet FR

**Auteur pédagogique : Zidane Djamal A**  
**Rôle : Architecte Oracle Infrastructure, HA/DR et formateur technique**  
**Dépôt cible : `zdmooc/oracle-exadata-infra-ha-dr-course-labs`**

Ce dépôt constitue un support de formation complet en français autour d’**Oracle Exadata Database Machine Administration Workshop**. Il est aligné sur les thèmes publiés par Oracle University pour le cours officiel et enrichi par une approche **infrastructure-first** : architecture, site planning, OEDA/OECA, storage/ASM, IORM, performance, Smart Scan, migration, Bulk Data Loading, monitoring détaillé, sauvegarde, HA/DR, patching, Automated Support Ecosystem, Exadata Cloud Service et Cloud@Customer [1].

> Ce dépôt est un support pédagogique indépendant. Il ne remplace ni Oracle University, ni la documentation Oracle, ni les procédures validées d’une organisation. Les commandes fournies sont majoritairement des commandes de **lecture non destructives**. Toute action de patching, modification, suppression, redémarrage ou reconfiguration doit être traitée comme risquée et validée dans un environnement de test.

## Structure du dépôt

| Dossier | Contenu |
|---|---|
| `modules/` | 28 modules numérotés de `00` à `27`, chacun avec objectifs, concepts, architecture, commandes read-only, bonnes pratiques, mini-lab et validation. |
| `labs/` | Travaux pratiques complets avec objectif, prérequis, contexte, commandes indicatives, résultat attendu, validation, nettoyage, risques et livrable. |
| `docs/` | Mapping Oracle University, glossaire Exadata, critères de complétude, rapport final, références et rôle auteur. |
| `templates/` | Modèles opérationnels : site planning, migration, Bulk Data Loading, monitoring, patching, SR support, Cloud@Customer. |
| `diagrams/` | Diagrammes Mermaid couvrant architecture, monitoring, migration, patching, support et cloud. |
| `scripts/` | Scripts d’exemple read-only pour collecter inventaire, versions, métriques et rapports sans modification. |

## Modules du cours

| Module | Sujet |
|---:|---|
| 00 | [Introduction](modules/00-introduction.md) |
| 01 | [Overview](modules/01-overview.md) |
| 02 | [Architecture](modules/02-architecture.md) |
| 03 | [Key Capabilities](modules/03-key-capabilities.md) |
| 04 | [Site Planning et intégration datacenter](modules/04-site-planning-et-intégration-datacenter.md) |
| 05 | [Initial Configuration](modules/05-initial-configuration.md) |
| 06 | [Storage Server Configuration](modules/06-storage-server-configuration.md) |
| 07 | [ASM et modèle de stockage](modules/07-asm-et-modèle-de-stockage.md) |
| 08 | [IORM](modules/08-iorm.md) |
| 09 | [Performance Recommendations](modules/09-performance-recommendations.md) |
| 10 | [Smart Scan](modules/10-smart-scan.md) |
| 11 | [Consolidation](modules/11-consolidation.md) |
| 12 | [Migration to Exadata](modules/12-migration-to-exadata.md) |
| 13 | [Bulk Data Loading](modules/13-bulk-data-loading.md) |
| 14 | [Platform Monitoring](modules/14-platform-monitoring.md) |
| 15 | [Monitoring Exadata System Software](modules/15-monitoring-exadata-system-software.md) |
| 16 | [Enterprise Manager Cloud Control](modules/16-enterprise-manager-cloud-control.md) |
| 17 | [Monitoring Storage Servers](modules/17-monitoring-storage-servers.md) |
| 18 | [Monitoring DB Servers](modules/18-monitoring-db-servers.md) |
| 19 | [Monitoring Network](modules/19-monitoring-network.md) |
| 20 | [Monitoring Other Components](modules/20-monitoring-other-components.md) |
| 21 | [Other Monitoring Tools](modules/21-other-monitoring-tools.md) |
| 22 | [Backup and Recovery](modules/22-backup-and-recovery.md) |
| 23 | [HA/DR et MAA](modules/23-ha-dr-et-maa.md) |
| 24 | [Maintenance Tasks](modules/24-maintenance-tasks.md) |
| 25 | [Patching](modules/25-patching.md) |
| 26 | [Automated Support Ecosystem](modules/26-automated-support-ecosystem.md) |
| 27 | [Exadata Cloud Service et Cloud@Customer](modules/27-exadata-cloud-service-et-cloud-customer.md) |


## Dépôt complémentaire séparé

Le dépôt `https://github.com/zdmooc/oracle-infra-architecture-ha-dr-labs` reste un référentiel tiers séparé. Il peut être cité comme complément architecture/HA/DR, mais il n’est pas modifié par ce cours.

## Références officielles

[1]: https://education.oracle.com/exadata-database-machine-administration-workshop/courP_4599 "Oracle University — Exadata Database Machine Administration Workshop"
[2]: https://docs.oracle.com/en/engineered-systems/exadata-database-machine/ "Oracle Exadata Database Machine Documentation"
[3]: https://docs.oracle.com/en/engineered-systems/exadata-database-machine/sagug/ "Oracle Exadata System Software User's Guide"
[4]: https://docs.oracle.com/en/engineered-systems/exadata-database-machine/dbmmn/ "Oracle Exadata Database Machine Maintenance Guide"
[5]: https://docs.oracle.com/en/database/oracle/oracle-database/ "Oracle Database Documentation"
[6]: https://www.oracle.com/database/maximum-availability-architecture/ "Oracle Maximum Availability Architecture"
[7]: https://docs.oracle.com/en/cloud/paas/exadata-cloud/ "Oracle Exadata Cloud Service Documentation"
[8]: https://docs.oracle.com/en/cloud/cloud-at-customer/exadata-cloud-at-customer/ "Oracle Exadata Cloud@Customer Documentation"
