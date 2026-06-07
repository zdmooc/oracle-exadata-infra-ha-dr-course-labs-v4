# Matrice Bulk Data Loading Exadata

| Méthode | Cas d’usage | Prérequis | Risques | Validation | Rollback |
|---|---|---|---|---|---|
| External Table | Lecture/chargement fichiers structurés | Directory, droits, format stable | Rejets format, performance si mauvaise parallélisation | Table rejet, count, checksums | Supprimer tables staging si approuvé |
| SQL Loader direct path | Chargement massif contrôlé | Control file, logs, bad files | Index/contraintes, espace undo/temp | Lignes chargées/rejetées | Table staging + truncate approuvé |
| Data Pump | Migration schéma/table | Dump, compatibilité version | Temps import, remap, stats | Logs impdp, objets invalides | Drop objets importés seulement via runbook |
| DBFS staging | Partage fichiers Exadata | DBFS configuré | Saturation staging | Espace et logs | Purge staging approuvée |
| CTAS / INSERT APPEND | Transformation in-database | Espace, stats, NOLOGGING contrôlé | Recoverability si NOLOGGING | Counts, stats, backup après | Drop/rename via CAB |
