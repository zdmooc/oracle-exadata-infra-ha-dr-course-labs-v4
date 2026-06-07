# Oracle Exadata Infrastructure HA/DR Course Labs — V3 française

Ce dépôt fournit un support de formation complet en français pour **Oracle Exadata Database Machine Administration Workshop**, avec une approche **infrastructure-first**, des modules techniques, des labs ciblés, des templates opérationnels, des diagrammes Mermaid, des runbooks et des scripts read-only.

Le dépôt tiers `https://github.com/zdmooc/oracle-infra-architecture-ha-dr-labs` reste séparé. Il peut être cité comme complément d’architecture, mais il n’est ni fusionné ni modifié par ce dépôt.

## Public visé

Ce cours s’adresse aux DBA Oracle confirmés, administrateurs Linux/Unix, architectes infrastructure, consultants Oracle, ingénieurs cloud/Exadata Cloud@Customer et équipes exploitation/support.

## Modules

| Module | Titre | Alignement Oracle University |
|---|---|---|
| 00 | [Introduction](modules/00-introduction.md) | Introduction |
| 01 | [Overview](modules/01-overview.md) | Overview |
| 02 | [Architecture](modules/02-architecture.md) | Architecture |
| 03 | [Key Capabilities](modules/03-key-capabilities.md) | Key Capabilities |
| 04 | [Site planning et intégration datacenter](modules/04-site-planning-et-integration-datacenter.md) | Initial Configuration |
| 05 | [Initial Configuration](modules/05-initial-configuration.md) | Initial Configuration |
| 06 | [Exadata Storage Server Configuration](modules/06-exadata-storage-server-configuration.md) | Exadata Storage Server Configuration |
| 07 | [ASM et modèle de stockage](modules/07-asm-et-modele-de-stockage.md) | Exadata Storage Server Configuration |
| 08 | [IORM](modules/08-iorm.md) | IORM |
| 09 | [Performance Recommendations](modules/09-performance-recommendations.md) | Performance Recommendations |
| 10 | [Smart Scan](modules/10-smart-scan.md) | Smart Scan |
| 11 | [Consolidation](modules/11-consolidation.md) | Consolidation |
| 12 | [Migration to Exadata](modules/12-migration-to-exadata.md) | Migration to Exadata |
| 13 | [Bulk Data Loading](modules/13-bulk-data-loading.md) | Bulk Data Loading |
| 14 | [Platform Monitoring Introduction](modules/14-platform-monitoring-introduction.md) | Platform Monitoring |
| 15 | [Monitoring Exadata System Software](modules/15-monitoring-exadata-system-software.md) | Monitoring Exadata System Software |
| 16 | [Enterprise Manager Cloud Control](modules/16-enterprise-manager-cloud-control.md) | Enterprise Manager Cloud Control |
| 17 | [Monitoring Storage Servers](modules/17-monitoring-storage-servers.md) | Monitoring Storage Servers |
| 18 | [Monitoring Database Servers](modules/18-monitoring-database-servers.md) | Monitoring DB Servers |
| 19 | [Monitoring Network](modules/19-monitoring-network.md) | Monitoring Other Components |
| 20 | [Monitoring Other Components](modules/20-monitoring-other-components.md) | Monitoring Other Components |
| 21 | [Other Monitoring Tools](modules/21-other-monitoring-tools.md) | Other Monitoring Tools |
| 22 | [Backup and Recovery](modules/22-backup-and-recovery.md) | Backup and Recovery |
| 23 | [HA/DR et MAA](modules/23-ha-dr-et-maa.md) | Backup and Recovery |
| 24 | [Maintenance Tasks](modules/24-maintenance-tasks.md) | Maintenance Tasks |
| 25 | [Patching](modules/25-patching.md) | Patching |
| 26 | [Automated Support Ecosystem](modules/26-automated-support-ecosystem.md) | Automated Support Ecosystem |
| 27 | [Exadata Cloud Service et Cloud@Customer](modules/27-exadata-cloud-service-et-cloud-customer.md) | Exadata Cloud Service / Cloud@Customer |

## Labs, templates, diagrammes et scripts

| Type | Contenu V3 |
|---|---:|
| Modules | 28 |
| Labs ciblés | 19 |
| Templates / runbooks | 27 |
| Diagrammes Mermaid | 13 |
| Scripts read-only | 9 |

## Contrôle qualité

Exécuter localement :

```bash
bash scripts/completeness-check.sh
bash scripts/dangerous-command-detector.sh
```

Les rapports principaux sont disponibles dans `docs/04-mapping-syllabus-oracle-university.md`, `docs/05-glossaire-exadata.md`, `docs/98-audit-contenu-generique.md` et `docs/99-rapport-completude-final.md`.
