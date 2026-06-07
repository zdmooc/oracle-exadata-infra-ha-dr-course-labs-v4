    # Module 01 — Overview

    ## Objectif du module

    Ce module permet de maîtriser **Vue d’ensemble Exadata, cas d’usage, composants et modèles de déploiement**. À la fin du module, l’apprenant doit savoir expliquer le sujet, identifier les composants Exadata concernés, collecter des preuves en lecture seule et produire un livrable exploitable par une équipe DBA, infrastructure, support ou cloud.

    ## Alignement avec le cours officiel

    Ce module couvre le thème Oracle University **Overview** du parcours **Exadata Database Machine Administration Workshop**. Il enrichit le thème avec une approche infrastructure-first, des commandes non destructives, des métriques observables et un mini-lab ciblé.

    ## Concepts clés

    | Concept | Explication opérationnelle |
    |---|---|
    | **Database Machine** | Élément à maîtriser dans ce module ; l’apprenant doit savoir le reconnaître, le relier à la couche Exadata concernée et produire une preuve observable. |
| **engineered system** | Élément à maîtriser dans ce module ; l’apprenant doit savoir le reconnaître, le relier à la couche Exadata concernée et produire une preuve observable. |
| **DB nodes** | Élément à maîtriser dans ce module ; l’apprenant doit savoir le reconnaître, le relier à la couche Exadata concernée et produire une preuve observable. |
| **storage cells** | Élément à maîtriser dans ce module ; l’apprenant doit savoir le reconnaître, le relier à la couche Exadata concernée et produire une preuve observable. |
| **scale-out** | Élément à maîtriser dans ce module ; l’apprenant doit savoir le reconnaître, le relier à la couche Exadata concernée et produire une preuve observable. |
| **offload** | Élément à maîtriser dans ce module ; l’apprenant doit savoir le reconnaître, le relier à la couche Exadata concernée et produire une preuve observable. |

    ## Architecture concernée

    Exadata assemble des serveurs de base, des cellules de stockage intelligentes, un réseau interne haut débit et une pile Oracle optimisée. L’overview clarifie la différence entre appliance intégrée, cluster RAC classique et service cloud.

    | Couche | Rôle dans ce module | Preuve typique |
    |---|---|---|
    | DB servers | Hébergent les instances, services, agents et outils Oracle. | `crsctl`, `srvctl`, vues `v$`/`gv$` si pertinent. |
    | Storage cells | Fournissent stockage intelligent, flash, offload, métriques et alertes. | `cellcli list ...` en lecture seule. |
    | ASM / Grid Infrastructure | Assure cluster, diskgroups, services et accès au stockage. | `asmcmd`, `crsctl`, vues ASM. |
    | Réseau Exadata | Transporte client, backup, administration et trafic privé. | Statistiques interfaces, routage, état fabric. |
    | Outils support | AHF, Exachk, TFA, EM selon le module. | Rapports santé, bundles, incidents, métriques. |

    ## Fonctionnement détaillé

    Le sujet doit être analysé par couches. L’approche recommandée consiste à formuler un symptôme, localiser la couche suspecte, collecter des preuves minimales, interpréter ces preuves, puis décider d’une action prudente. Le support ne propose pas de modification destructive par défaut. Toute action de changement, de patching, de redémarrage, de mise hors ligne ou de suppression doit être traitée dans un runbook validé et explicitement signalée comme risquée.

    Pour ce module, l’analyse doit rester spécifique à **Overview**. Les preuves attendues ne sont pas un simple inventaire système ; elles doivent démontrer la compréhension du mécanisme Exadata concerné, de ses dépendances et de ses limites.

    ## Commandes et vues utiles en lecture

    Les commandes suivantes sont fournies comme exemples de lecture. Elles doivent être adaptées à la version, aux privilèges et aux standards de l’environnement. Les commandes nécessitant des privilèges élevés sont indiquées en commentaire lorsqu’elles peuvent varier selon site.

    ```bash
    cellcli -e list cell detail
dcli -g dbs_group -l root "imageinfo"  # privilèges root requis
crsctl stat res -t
    ```

    ## Métriques à analyser

    | Métrique ou preuve | Interprétation prudente |
    |---|---|
    | version Exadata System Software | À comparer avec la période, le workload et la couche concernée ; aucun seuil universel n’est inventé dans ce support. |
| nombre de DB servers et cells | À comparer avec la période, le workload et la couche concernée ; aucun seuil universel n’est inventé dans ce support. |
| état CRS/RAC | À comparer avec la période, le workload et la couche concernée ; aucun seuil universel n’est inventé dans ce support. |
| alertes cellule ouvertes | À comparer avec la période, le workload et la couche concernée ; aucun seuil universel n’est inventé dans ce support. |

    ## Exemple d’analyse

    **Symptôme.** Une équipe reprend une plateforme inconnue. Elle doit identifier le modèle, les nœuds, les cellules, la version et les composants critiques avant toute analyse.

    **Couche suspecte.** La couche doit être choisie à partir du symptôme : base, ASM, storage cell, réseau, monitoring, sauvegarde, support ou cloud. L’analyse ne doit pas supposer la cause avant collecte.

    **Preuves à collecter.** Les preuves minimales sont les commandes et vues listées plus haut, complétées par l’heure de début, l’impact métier, le périmètre touché et l’état avant/après si disponible.

    **Interprétation.** Les résultats sont comparés avec un état de référence connu, une période équivalente ou les recommandations Oracle applicables. Le support évite d’inventer des seuils universels.

    **Prochaine action prudente.** Si l’action dépasse la lecture, produire un runbook, obtenir validation CAB ou support, et documenter rollback, impact et communication.

    ## Erreurs fréquentes

    | Erreur spécifique | Correction recommandée |
    |---|---|
    | documenter uniquement les bases et oublier cells/switches | Produire une preuve, relire le runbook et escalader si l’action dépasse la lecture. |
| raisonner stockage SAN alors que les grid disks sont fournis par cells | Produire une preuve, relire le runbook et escalader si l’action dépasse la lecture. |
| ignorer la version image lors d’un diagnostic | Produire une preuve, relire le runbook et escalader si l’action dépasse la lecture. |

    ## Bonnes pratiques

    | Bonne pratique | Mise en œuvre |
    |---|---|
    | commencer par inventaire read-only | À intégrer dans le livrable du module. |
| corréler DB, GI et cells | À intégrer dans le livrable du module. |
| conserver une photo de référence de la plateforme | À intégrer dans le livrable du module. |

    ## Mini-lab ciblé

    **Objectif.** Construire une fiche d’inventaire overview avec rôles DB/cell, versions, état GI et composants visibles.

    **Étapes.** L’apprenant prépare un dossier de travail, exécute uniquement les commandes read-only adaptées à son environnement, capture les sorties horodatées, interprète les métriques propres au module et rédige une conclusion. Aucune commande de suppression, redémarrage, patching, offline/drop ou modification de paramètre n’est autorisée dans ce mini-lab.

    **Résultat attendu.** Le résultat doit relier un symptôme ou un objectif pédagogique à des preuves Exadata spécifiques, et non à un simple inventaire générique.

    ## Questions de validation

    1. Quels composants différencient Exadata d’un RAC sur stockage externe ?
2. Pourquoi l’inventaire version est-il obligatoire avant support ?

    ## Livrables attendus

    Tableau overview plateforme.


## Diagrammes associés

- [`architecture-globale-exadata.mmd`](../diagrams/architecture-globale-exadata.mmd)
- [`rack-db-servers-storage-cells.mmd`](../diagrams/rack-db-servers-storage-cells.mmd)

## Références officielles

Les références ci-dessous doivent être utilisées comme point d'entrée, puis ajustées selon la génération Exadata, la version Oracle Database et le modèle de service utilisé.

| Référence | Usage |
|---|---|
| [Oracle University — Exadata Database Machine Administration Workshop](https://education.oracle.com/exadata-database-machine-administration-workshop/courP_4599) | Alignement pédagogique du workshop. |
| [Oracle Exadata System Software Documentation](https://docs.oracle.com/en/engineered-systems/exadata-database-machine/) | Administration Exadata, Storage Server, outils et maintenance. |
| [Oracle Maximum Availability Architecture](https://www.oracle.com/database/technologies/high-availability/maa.html) | HA/DR, Data Guard, sauvegarde, meilleures pratiques. |
| [Oracle Database Backup and Recovery User's Guide](https://docs.oracle.com/en/database/) | RMAN, restauration, récupération et validation. |
| [Oracle Autonomous Health Framework](https://docs.oracle.com/en/engineered-systems/health-diagnostics/autonomous-health-framework/) | AHF, ORAchk, Exachk et TFA. |

