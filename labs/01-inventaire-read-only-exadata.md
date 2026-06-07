# Lab 01 — Inventaire read-only Exadata

## Objectif

Ce lab vise à collecter hôtes, versions, services, cellules, ASM et bases sans modification. Il est conçu pour être exécuté en priorité en environnement de formation ou de préproduction. Les commandes sont indicatives et doivent être adaptées à votre version et à vos droits.

## Prérequis

| Élément | Exigence |
|---|---|
| Accès | Compte disposant des droits de lecture nécessaires sur les hôtes concernés. |
| Documentation | Documentation de version Oracle Exadata, Oracle Database et procédures internes. |
| Sécurité | Interdiction d’exécuter une commande de modification sans validation formelle. |
| Sorties | Répertoire de collecte horodaté, sans secret ni mot de passe. |

## Contexte

L’administrateur doit produire une preuve exploitable par une équipe DBA, infrastructure ou support. Le lab privilégie l’observation, la classification des informations et la rédaction d’une conclusion.

## Commandes indicatives

```bash
mkdir -p evidence/lab-01-$(date +%Y%m%d-%H%M%S)
hostname -f
date
uname -a
ip -br addr
df -h
crsctl stat res -t
srvctl status database -v
asmcmd lsdg
# Sur cellule storage, si autorisé :
cellcli -e list cell detail
cellcli -e list alerthistory
cellcli -e list metriccurrent
```

## Résultat attendu

| Preuve | Attendu |
|---|---|
| Inventaire | Hôtes, rôles, versions et composants clairement identifiés. |
| État | Services et objets observés sans modification. |
| Analyse | Écarts, alertes, risques ou inconnues documentés. |
| Synthèse | Conclusion exploitable par une équipe opérationnelle. |

## Validation

La validation consiste à relire les sorties, vérifier l’absence de secret, confirmer que les commandes exécutées sont non destructives et produire une synthèse courte. Le formateur peut demander à l’apprenant d’expliquer quelle couche Exadata est concernée et quelles actions seraient risquées.

## Nettoyage

Aucun nettoyage technique destructif n’est requis. Il faut seulement archiver les preuves autorisées, supprimer les copies contenant des informations sensibles et conserver le rapport final dans l’espace prévu par l’organisation.

## Risques

| Risque | Mesure de maîtrise |
|---|---|
| Exécution avec privilèges excessifs | Limiter aux commandes de lecture et enregistrer les commandes exécutées. |
| Collecte de secrets | Masquer mots de passe, tokens, chaînes de connexion et informations sensibles. |
| Mauvaise interprétation | Croiser les preuves avec documentation Oracle et procédures internes. |
| Transformation en procédure production | Faire valider tout runbook avant usage réel. |

## Livrable

Le livrable est un fichier Markdown ou PDF interne contenant contexte, commandes exécutées, sorties résumées, anomalies, risques, questions ouvertes et recommandations. Les fichiers bruts doivent être joints uniquement si leur diffusion est autorisée.

## Références officielles

[1]: https://education.oracle.com/exadata-database-machine-administration-workshop/courP_4599 "Oracle University — Exadata Database Machine Administration Workshop"
[2]: https://docs.oracle.com/en/engineered-systems/exadata-database-machine/ "Oracle Exadata Database Machine Documentation"
[3]: https://docs.oracle.com/en/engineered-systems/exadata-database-machine/sagug/ "Oracle Exadata System Software User's Guide"
[4]: https://docs.oracle.com/en/engineered-systems/exadata-database-machine/dbmmn/ "Oracle Exadata Database Machine Maintenance Guide"
[5]: https://docs.oracle.com/en/database/oracle/oracle-database/ "Oracle Database Documentation"
[6]: https://www.oracle.com/database/maximum-availability-architecture/ "Oracle Maximum Availability Architecture"
[7]: https://docs.oracle.com/en/cloud/paas/exadata-cloud/ "Oracle Exadata Cloud Service Documentation"
[8]: https://docs.oracle.com/en/cloud/cloud-at-customer/exadata-cloud-at-customer/ "Oracle Exadata Cloud@Customer Documentation"
