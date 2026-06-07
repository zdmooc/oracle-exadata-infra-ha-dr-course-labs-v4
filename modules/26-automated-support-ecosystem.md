    # Module 26 — Automated Support Ecosystem

    ## Objectif du module

    Ce module permet de maîtriser **AHF, Exachk, TFA, ORAchk, ASR, Service Request, collecte support et protection des logs**. À la fin du module, l’apprenant doit savoir expliquer le sujet, identifier les composants Exadata concernés, collecter des preuves en lecture seule et produire un livrable exploitable par une équipe DBA, infrastructure, support ou cloud.

    ## Alignement avec le cours officiel

    Ce module couvre le thème Oracle University **Automated Support Ecosystem** du parcours **Exadata Database Machine Administration Workshop**. Il enrichit le thème avec une approche infrastructure-first, des commandes non destructives, des métriques observables et un mini-lab ciblé.

    ## Concepts clés

    | Concept | Explication opérationnelle |
    |---|---|
    | **AHF** | Élément à maîtriser dans ce module ; l’apprenant doit savoir le reconnaître, le relier à la couche Exadata concernée et produire une preuve observable. |
| **Exachk** | Élément à maîtriser dans ce module ; l’apprenant doit savoir le reconnaître, le relier à la couche Exadata concernée et produire une preuve observable. |
| **TFA** | Élément à maîtriser dans ce module ; l’apprenant doit savoir le reconnaître, le relier à la couche Exadata concernée et produire une preuve observable. |
| **ORAchk** | Élément à maîtriser dans ce module ; l’apprenant doit savoir le reconnaître, le relier à la couche Exadata concernée et produire une preuve observable. |
| **ASR** | Élément à maîtriser dans ce module ; l’apprenant doit savoir le reconnaître, le relier à la couche Exadata concernée et produire une preuve observable. |
| **Service Request** | Élément à maîtriser dans ce module ; l’apprenant doit savoir le reconnaître, le relier à la couche Exadata concernée et produire une preuve observable. |
| **diagnostic bundle** | Élément à maîtriser dans ce module ; l’apprenant doit savoir le reconnaître, le relier à la couche Exadata concernée et produire une preuve observable. |
| **log sanitization** | Élément à maîtriser dans ce module ; l’apprenant doit savoir le reconnaître, le relier à la couche Exadata concernée et produire une preuve observable. |

    ## Architecture concernée

    L’écosystème support automatise vérifications, collecte, détection et ouverture de support selon configuration. Il ne dispense pas d’une revue sécurité ni d’un dossier SR structuré.

    | Couche | Rôle dans ce module | Preuve typique |
    |---|---|---|
    | DB servers | Hébergent les instances, services, agents et outils Oracle. | `crsctl`, `srvctl`, vues `v$`/`gv$` si pertinent. |
    | Storage cells | Fournissent stockage intelligent, flash, offload, métriques et alertes. | `cellcli list ...` en lecture seule. |
    | ASM / Grid Infrastructure | Assure cluster, diskgroups, services et accès au stockage. | `asmcmd`, `crsctl`, vues ASM. |
    | Réseau Exadata | Transporte client, backup, administration et trafic privé. | Statistiques interfaces, routage, état fabric. |
    | Outils support | AHF, Exachk, TFA, EM selon le module. | Rapports santé, bundles, incidents, métriques. |

    ## Fonctionnement détaillé

    Le sujet doit être analysé par couches. L’approche recommandée consiste à formuler un symptôme, localiser la couche suspecte, collecter des preuves minimales, interpréter ces preuves, puis décider d’une action prudente. Le support ne propose pas de modification destructive par défaut. Toute action de changement, de patching, de redémarrage, de mise hors ligne ou de suppression doit être traitée dans un runbook validé et explicitement signalée comme risquée.

    Pour ce module, l’analyse doit rester spécifique à **Automated Support Ecosystem**. Les preuves attendues ne sont pas un simple inventaire système ; elles doivent démontrer la compréhension du mécanisme Exadata concerné, de ses dépendances et de ses limites.

    ## Commandes et vues utiles en lecture

    Les commandes suivantes sont fournies comme exemples de lecture. Elles doivent être adaptées à la version, aux privilèges et aux standards de l’environnement. Les commandes nécessitant des privilèges élevés sont indiquées en commentaire lorsqu’elles peuvent varier selon site.

    ```bash
    ahfctl status
tfactl print status
tfactl diagcollect -from "YYYY-MM-DD HH24:MI" -to "YYYY-MM-DD HH24:MI"  # cadrer période et revue sécurité
exachk -v
asr show_status  # si ASR installé/configuré
    ```

    ## Métriques à analyser

    | Métrique ou preuve | Interprétation prudente |
    |---|---|
    | état AHF/TFA | À comparer avec la période, le workload et la couche concernée ; aucun seuil universel n’est inventé dans ce support. |
| version Exachk | À comparer avec la période, le workload et la couche concernée ; aucun seuil universel n’est inventé dans ce support. |
| présence ASR | À comparer avec la période, le workload et la couche concernée ; aucun seuil universel n’est inventé dans ce support. |
| taille bundle | À comparer avec la période, le workload et la couche concernée ; aucun seuil universel n’est inventé dans ce support. |
| période collecte | À comparer avec la période, le workload et la couche concernée ; aucun seuil universel n’est inventé dans ce support. |
| liste fichiers sensibles | À comparer avec la période, le workload et la couche concernée ; aucun seuil universel n’est inventé dans ce support. |

    ## Exemple d’analyse

    **Symptôme.** Incident cell ou DB critique : préparer un SR avec symptômes, impact, timeline, Exachk/TFA ciblés et preuves nettoyées.

    **Couche suspecte.** La couche doit être choisie à partir du symptôme : base, ASM, storage cell, réseau, monitoring, sauvegarde, support ou cloud. L’analyse ne doit pas supposer la cause avant collecte.

    **Preuves à collecter.** Les preuves minimales sont les commandes et vues listées plus haut, complétées par l’heure de début, l’impact métier, le périmètre touché et l’état avant/après si disponible.

    **Interprétation.** Les résultats sont comparés avec un état de référence connu, une période équivalente ou les recommandations Oracle applicables. Le support évite d’inventer des seuils universels.

    **Prochaine action prudente.** Si l’action dépasse la lecture, produire un runbook, obtenir validation CAB ou support, et documenter rollback, impact et communication.

    ## Erreurs fréquentes

    | Erreur spécifique | Correction recommandée |
    |---|---|
    | envoyer secrets dans logs | Produire une preuve, relire le runbook et escalader si l’action dépasse la lecture. |
| collecter période trop large | Produire une preuve, relire le runbook et escalader si l’action dépasse la lecture. |
| ouvrir SR sans impact métier | Produire une preuve, relire le runbook et escalader si l’action dépasse la lecture. |
| confondre ASR et résolution automatique | Produire une preuve, relire le runbook et escalader si l’action dépasse la lecture. |

    ## Bonnes pratiques

    | Bonne pratique | Mise en œuvre |
    |---|---|
    | template SR | À intégrer dans le livrable du module. |
| sanitization | À intégrer dans le livrable du module. |
| collecte minimale suffisante | À intégrer dans le livrable du module. |
| traçabilité upload | À intégrer dans le livrable du module. |

    ## Mini-lab ciblé

    **Objectif.** Préparer un dossier support sans données sensibles avec checklist SR et commandes AHF/TFA.

    **Étapes.** L’apprenant prépare un dossier de travail, exécute uniquement les commandes read-only adaptées à son environnement, capture les sorties horodatées, interprète les métriques propres au module et rédige une conclusion. Aucune commande de suppression, redémarrage, patching, offline/drop ou modification de paramètre n’est autorisée dans ce mini-lab.

    **Résultat attendu.** Le résultat doit relier un symptôme ou un objectif pédagogique à des preuves Exadata spécifiques, et non à un simple inventaire générique.

    ## Questions de validation

    1. Quel rôle joue ASR ?
2. Pourquoi revoir les logs avant upload ?

    ## Livrables attendus

    Template SR et matrice collecte support.


## Diagrammes associés

- [`support-ecosystem.mmd`](../diagrams/support-ecosystem.mmd)

## Références officielles

Les références ci-dessous doivent être utilisées comme point d'entrée, puis ajustées selon la génération Exadata, la version Oracle Database et le modèle de service utilisé.

| Référence | Usage |
|---|---|
| [Oracle University — Exadata Database Machine Administration Workshop](https://education.oracle.com/exadata-database-machine-administration-workshop/courP_4599) | Alignement pédagogique du workshop. |
| [Oracle Exadata System Software Documentation](https://docs.oracle.com/en/engineered-systems/exadata-database-machine/) | Administration Exadata, Storage Server, outils et maintenance. |
| [Oracle Maximum Availability Architecture](https://www.oracle.com/database/technologies/high-availability/maa.html) | HA/DR, Data Guard, sauvegarde, meilleures pratiques. |
| [Oracle Database Backup and Recovery User's Guide](https://docs.oracle.com/en/database/) | RMAN, restauration, récupération et validation. |
| [Oracle Autonomous Health Framework](https://docs.oracle.com/en/engineered-systems/health-diagnostics/autonomous-health-framework/) | AHF, ORAchk, Exachk et TFA. |

