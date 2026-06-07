# Module 22 — Backup and Recovery

**Alignement Oracle University :** Backup and Recovery.  
**Auteur pédagogique :** Zidane Djamal A.  
**Positionnement :** cours français indépendant, infrastructure-first, aligné sur les thèmes publiés du workshop Oracle University [1].

## Objectifs

À la fin de ce module, l’apprenant doit pouvoir expliquer le périmètre **Backup and Recovery**, le relier aux composants Exadata concernés, identifier les commandes de lecture utiles, formuler les risques principaux et produire un livrable d’exploitation vérifiable.

| Objectif | Résultat attendu |
|---|---|
| Comprendre le thème | L’apprenant décrit les composants, services ou pratiques concernés sans confondre base, serveur DB, cellule storage et réseau. |
| Lire l’état courant | L’apprenant collecte des preuves non destructives et sait les classer. |
| Détecter les risques | L’apprenant repère les erreurs fréquentes, lacunes de supervision et dépendances opérationnelles. |
| Produire un livrable | L’apprenant remet une fiche de synthèse utilisable par une équipe DBA/infra. |

## Concepts

La sauvegarde et la restauration doivent être conçues avec RMAN, FRA/RECO, catalogues, rétention, tests de restore, Data Guard, encryption et contraintes de performance. Le module privilégie l’audit de configuration et les validations non destructives [5] [6].

Dans ce cours, le terme **infrastructure-first** signifie que chaque sujet est traité depuis les couches physiques et opérationnelles vers les services Oracle Database. Cette approche évite de réduire Exadata à une base de données rapide : elle met en relation datacenter, réseau, compute, storage, ASM, Clusterware, supervision, support, sécurité et continuité.

## Architecture concernée

| Couche | Éléments à observer | Pourquoi c’est important |
|---|---|---|
| Datacenter | Rack, alimentation, câblage, accès management | Les incidents physiques et les erreurs de câblage peuvent produire des symptômes applicatifs. |
| Réseau | Client, backup, management, interconnexion interne | Les chemins réseau conditionnent migration, backup, supervision et latence. |
| Compute | Serveurs DB, OS, Grid Infrastructure, ASM, Oracle Database | Les bases s’appuient sur cette couche pour RAC, services, listeners et accès aux diskgroups. |
| Storage | Cellules, cell disks, grid disks, flash, alertes | Les optimisations Exadata et la résilience ASM dépendent de cette couche. |
| Exploitation | Monitoring, patching, support, runbooks | La qualité opérationnelle réduit le temps de diagnostic et le risque de changement. |

## Explications détaillées

Le module doit être travaillé avec un environnement de formation, une documentation de version et des accès en lecture. Les commandes proposées ci-dessous servent à **observer**. Elles ne modifient pas la configuration, ne redémarrent aucun service, ne suppriment aucun objet et ne changent aucun paramètre. Les actions de correction, patching, reconfiguration ou suppression doivent toujours être traitées dans un runbook approuvé.

## Commandes de lecture non destructives

```bash
# Lecture seule : hostname -f
# Lecture seule : date
# Lecture seule : uname -a
# Lecture seule : df -h
# Lecture seule : ip -br addr
# Lecture seule : srvctl status database -v
# Lecture seule : crsctl stat res -t
# Lecture seule : asmcmd lsdg
# Lecture seule : sqlplus -L / as sysdba
# Lecture seule : select name, open_mode, database_role from v$database;
# Lecture seule : select inst_id, instance_name, status from gv$instance;
```

> **Attention :** certaines commandes comme `sqlplus / as sysdba`, `cellcli`, `dcli`, `crsctl` ou `srvctl` peuvent nécessiter des privilèges élevés. Dans ce cours, elles sont utilisées uniquement pour lire l’état. Toute commande avec `modify`, `alter`, `drop`, `delete`, `restart`, `shutdown`, `startup`, `patch`, `apply` ou `rebalance` doit être considérée comme potentiellement risquée.

## Points de vigilance

| Point | Vigilance opérationnelle |
|---|---|
| Version | Toujours rattacher une observation à une version Exadata System Software, Grid Infrastructure et Oracle Database. |
| Portée | Distinguer lecture locale, lecture cellule, lecture cluster et lecture base. |
| Horodatage | Horodater les collectes pour comparer avant/après incident ou changement. |
| Privilèges | Utiliser le moindre privilège compatible avec la collecte demandée. |
| Production | Ne jamais transformer un lab en procédure production sans validation interne et documentation Oracle de version. |

## Erreurs fréquentes

| Erreur | Impact | Prévention |
|---|---|---|
| Confondre cellule storage et serveur DB | Mauvais diagnostic et escalade retardée | Toujours indiquer la couche concernée. |
| Collecter sans contexte | Données difficiles à interpréter | Ajouter date, hôte, rôle, version et symptôme. |
| Appliquer une commande trouvée en ligne | Risque de changement non maîtrisé | Privilégier la documentation Oracle et les runbooks validés. |
| Ignorer le réseau | Symptômes de performance mal attribués | Inclure réseau client, backup, management et interne dans l’analyse. |

## Bonnes pratiques

L’équipe doit maintenir un inventaire vivant, une matrice réseau, une cartographie des responsabilités, un calendrier de maintenance, des preuves de sauvegarde, un historique de patching, des modèles de SR support et des procédures de validation après changement. Les preuves doivent être stockées dans un espace d’exploitation contrôlé avec nommage stable.

## Mini-lab

| Étape | Action | Résultat attendu |
|---:|---|---|
| 1 | Identifier les hôtes et rôles concernés par le thème. | Liste des serveurs DB, cellules ou composants supervisés. |
| 2 | Exécuter uniquement les commandes de lecture adaptées à votre environnement. | Fichiers de sortie horodatés. |
| 3 | Classer les informations par couche : compute, storage, réseau, base, support. | Tableau de synthèse clair. |
| 4 | Comparer avec les attentes du module. | Écarts, risques et questions ouvertes. |

## Questions de validation

| Question | Critère de bonne réponse |
|---|---|
| Quelle couche Exadata est principalement concernée par ce module ? | La réponse distingue compute, storage, réseau, base et exploitation. |
| Quelles preuves collecter avant d’ouvrir un incident ? | La réponse inclut symptômes, horodatage, versions, logs ou métriques. |
| Quelle commande serait risquée dans ce contexte ? | La réponse identifie les verbes de modification et propose une alternative de lecture. |
| Quel livrable remettre à une équipe d’exploitation ? | La réponse propose une fiche structurée, vérifiable et exploitable. |

## Livrables attendus

| Livrable | Format recommandé |
|---|---|
| Note de synthèse du module | Markdown ou document interne. |
| Sorties de commandes | Fichiers texte horodatés, sans secret. |
| Tableau de risques | Liste des écarts, sévérité, propriétaire, action. |
| Questions restantes | Liste transmise au formateur ou à l’équipe référente. |

## Références officielles

[1]: https://education.oracle.com/exadata-database-machine-administration-workshop/courP_4599 "Oracle University — Exadata Database Machine Administration Workshop"
[2]: https://docs.oracle.com/en/engineered-systems/exadata-database-machine/ "Oracle Exadata Database Machine Documentation"
[3]: https://docs.oracle.com/en/engineered-systems/exadata-database-machine/sagug/ "Oracle Exadata System Software User's Guide"
[4]: https://docs.oracle.com/en/engineered-systems/exadata-database-machine/dbmmn/ "Oracle Exadata Database Machine Maintenance Guide"
[5]: https://docs.oracle.com/en/database/oracle/oracle-database/ "Oracle Database Documentation"
[6]: https://www.oracle.com/database/maximum-availability-architecture/ "Oracle Maximum Availability Architecture"
[7]: https://docs.oracle.com/en/cloud/paas/exadata-cloud/ "Oracle Exadata Cloud Service Documentation"
[8]: https://docs.oracle.com/en/cloud/cloud-at-customer/exadata-cloud-at-customer/ "Oracle Exadata Cloud@Customer Documentation"
