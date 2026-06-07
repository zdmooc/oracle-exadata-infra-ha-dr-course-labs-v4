# Matrice réseau Exadata

| Interface / Réseau | Usage | VLAN | CIDR | MTU | DNS | Gateway | Firewall | Owner |
|---|---|---|---|---:|---|---|---|---|
| Admin | Management, SSH, ILOM | À compléter | À compléter | 1500 | Oui/Non | À compléter | À compléter | Infra |
| Client | Accès applicatif et services DB | À compléter | À compléter | 1500/9000 | Oui | À compléter | À compléter | Réseau/DBA |
| Backup | Sauvegarde et restore | À compléter | À compléter | 9000 si validé | Selon design | À compléter | À compléter | Backup |
| Interconnect | Cluster et DB-storage fabric | N/A | Privé | Selon génération | Non | N/A | Isolé | Oracle/Infra |
