# Oracle Exadata Database Machine Administration Workshop — Support de cours français V4

Ce dépôt contient une V4 orientée **cours complet** et non plus seulement audit ou exploitation. Chaque module est réécrit comme un chapitre pédagogique avec objectifs, concepts définis, fonctionnement interne, architecture, exemple réaliste, commandes, interprétation, erreurs fréquentes, bonnes pratiques, exercice et corrigé.

Le dépôt tiers `https://github.com/zdmooc/oracle-infra-architecture-ha-dr-labs` reste séparé et n’a pas été modifié. Il peut être cité comme complément d’architecture infrastructure/HA/DR, mais ce dépôt porte le cours Exadata.

## Modules V4

| Module | Titre | Statut |
|---|---|---|
| 00 | [Introduction au workshop Exadata](modules/00-introduction-au-workshop-exadata.md) | Chapitre pédagogique complet avec exemple et corrigé. |
| 01 | [Overview](modules/01-overview.md) | Chapitre pédagogique complet avec exemple et corrigé. |
| 02 | [Architecture](modules/02-architecture.md) | Chapitre pédagogique complet avec exemple et corrigé. |
| 03 | [Key Capabilities](modules/03-key-capabilities.md) | Chapitre pédagogique complet avec exemple et corrigé. |
| 04 | [Site planning et intégration datacenter](modules/04-site-planning-et-integration-datacenter.md) | Chapitre pédagogique complet avec exemple et corrigé. |
| 05 | [Initial Configuration](modules/05-initial-configuration.md) | Chapitre pédagogique complet avec exemple et corrigé. |
| 06 | [Exadata Storage Server Configuration](modules/06-exadata-storage-server-configuration.md) | Chapitre pédagogique complet avec exemple et corrigé. |
| 07 | [ASM et modèle de stockage](modules/07-asm-et-modele-de-stockage.md) | Chapitre pédagogique complet avec exemple et corrigé. |
| 08 | [IORM](modules/08-iorm.md) | Chapitre pédagogique complet avec exemple et corrigé. |
| 09 | [Performance Recommendations](modules/09-performance-recommendations.md) | Chapitre pédagogique complet avec exemple et corrigé. |
| 10 | [Smart Scan](modules/10-smart-scan.md) | Chapitre pédagogique complet avec exemple et corrigé. |
| 11 | [Consolidation](modules/11-consolidation.md) | Chapitre pédagogique complet avec exemple et corrigé. |
| 12 | [Migration to Exadata](modules/12-migration-to-exadata.md) | Chapitre pédagogique complet avec exemple et corrigé. |
| 13 | [Bulk Data Loading](modules/13-bulk-data-loading.md) | Chapitre pédagogique complet avec exemple et corrigé. |
| 14 | [Platform Monitoring Introduction](modules/14-platform-monitoring-introduction.md) | Chapitre pédagogique complet avec exemple et corrigé. |
| 15 | [Monitoring Exadata System Software](modules/15-monitoring-exadata-system-software.md) | Chapitre pédagogique complet avec exemple et corrigé. |
| 16 | [Enterprise Manager Cloud Control](modules/16-enterprise-manager-cloud-control.md) | Chapitre pédagogique complet avec exemple et corrigé. |
| 17 | [Monitoring Storage Servers](modules/17-monitoring-storage-servers.md) | Chapitre pédagogique complet avec exemple et corrigé. |
| 18 | [Monitoring Database Servers](modules/18-monitoring-database-servers.md) | Chapitre pédagogique complet avec exemple et corrigé. |
| 19 | [Monitoring Network](modules/19-monitoring-network.md) | Chapitre pédagogique complet avec exemple et corrigé. |
| 20 | [Monitoring Other Components](modules/20-monitoring-other-components.md) | Chapitre pédagogique complet avec exemple et corrigé. |
| 21 | [Other Monitoring Tools](modules/21-other-monitoring-tools.md) | Chapitre pédagogique complet avec exemple et corrigé. |
| 22 | [Backup and Recovery](modules/22-backup-and-recovery.md) | Chapitre pédagogique complet avec exemple et corrigé. |
| 23 | [HA/DR et MAA](modules/23-ha-dr-et-maa.md) | Chapitre pédagogique complet avec exemple et corrigé. |
| 24 | [Maintenance Tasks](modules/24-maintenance-tasks.md) | Chapitre pédagogique complet avec exemple et corrigé. |
| 25 | [Patching](modules/25-patching.md) | Chapitre pédagogique complet avec exemple et corrigé. |
| 26 | [Automated Support Ecosystem](modules/26-automated-support-ecosystem.md) | Chapitre pédagogique complet avec exemple et corrigé. |
| 27 | [Exadata Cloud Service et Cloud@Customer](modules/27-exadata-cloud-service-et-cloud-customer.md) | Chapitre pédagogique complet avec exemple et corrigé. |

## Contenu du dépôt

| Élément | Nombre |
|---|---:|
| Modules pédagogiques | 28 |
| Labs ciblés | 19 |
| Templates / runbooks | 27 |
| Diagrammes Mermaid | 13 |
| Scripts read-only | 9 |

## Contrôle qualité

```bash
bash scripts/completeness-check.sh
bash scripts/dangerous-command-detector.sh
```
