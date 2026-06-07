# Matrice stratégie de migration vers Exadata

| Méthode | Downtime typique | Volume adapté | Avantages | Risques | Fallback |
|---|---|---|---|---|---|
| Data Pump | Moyen à élevé | Petit à moyen | Simple, filtrage objets | Durée import/export, stats | Réouvrir source si cutover non validé |
| RMAN Duplicate | Moyen | Moyen à grand | Copie physique cohérente | Version/plateforme, réseau | Conserver source intacte |
| TTS / XTTS | Faible à moyen | Grand | Réduit déplacement logique | Complexité, contraintes platform | Revenir source, relancer incrémentaux |
| Data Guard | Faible | Grand critique | Cutover contrôlé, rollback possible avant failover | Préparation forte, compatibilité | Garder primaire tant que switchover non validé |
| GoldenGate / ZDM | Très faible | Critique | Migration progressive | Complexité, validation applicative | Bascule inverse planifiée |
