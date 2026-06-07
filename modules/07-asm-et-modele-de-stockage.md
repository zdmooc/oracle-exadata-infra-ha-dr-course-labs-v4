    # Module 07 — ASM et modèle de stockage

    ## Objectif du module

    Ce module permet de maîtriser **Mapping physical disk, cell disk, grid disk, ASM diskgroup, redondance et rebalance**. À la fin du module, l’apprenant doit savoir expliquer le sujet, identifier les composants Exadata concernés, collecter des preuves en lecture seule et produire un livrable exploitable par une équipe DBA, infrastructure, support ou cloud.

    ## Alignement avec le cours officiel

    Ce module couvre le thème Oracle University **Exadata Storage Server Configuration** du parcours **Exadata Database Machine Administration Workshop**. Il enrichit le thème avec une approche infrastructure-first, des commandes non destructives, des métriques observables et un mini-lab ciblé.

    ## Concepts clés

    | Concept | Explication opérationnelle |
    |---|---|
    | **ASM diskgroup** | Élément à maîtriser dans ce module ; l’apprenant doit savoir le reconnaître, le relier à la couche Exadata concernée et produire une preuve observable. |
| **grid disk** | Élément à maîtriser dans ce module ; l’apprenant doit savoir le reconnaître, le relier à la couche Exadata concernée et produire une preuve observable. |
| **failure group** | Élément à maîtriser dans ce module ; l’apprenant doit savoir le reconnaître, le relier à la couche Exadata concernée et produire une preuve observable. |
| **rebalance** | Élément à maîtriser dans ce module ; l’apprenant doit savoir le reconnaître, le relier à la couche Exadata concernée et produire une preuve observable. |
| **allocation unit** | Élément à maîtriser dans ce module ; l’apprenant doit savoir le reconnaître, le relier à la couche Exadata concernée et produire une preuve observable. |
| **redundancy** | Élément à maîtriser dans ce module ; l’apprenant doit savoir le reconnaître, le relier à la couche Exadata concernée et produire une preuve observable. |

    ## Architecture concernée

    ASM consomme des grid disks venant des cells. Les failure groups reflètent la résilience. L’analyse doit croiser ASM et CellCLI pour éviter les conclusions partielles.

    | Couche | Rôle dans ce module | Preuve typique |
    |---|---|---|
    | DB servers | Hébergent les instances, services, agents et outils Oracle. | `crsctl`, `srvctl`, vues `v$`/`gv$` si pertinent. |
    | Storage cells | Fournissent stockage intelligent, flash, offload, métriques et alertes. | `cellcli list ...` en lecture seule. |
    | ASM / Grid Infrastructure | Assure cluster, diskgroups, services et accès au stockage. | `asmcmd`, `crsctl`, vues ASM. |
    | Réseau Exadata | Transporte client, backup, administration et trafic privé. | Statistiques interfaces, routage, état fabric. |
    | Outils support | AHF, Exachk, TFA, EM selon le module. | Rapports santé, bundles, incidents, métriques. |

    ## Fonctionnement détaillé

    Le sujet doit être analysé par couches. L’approche recommandée consiste à formuler un symptôme, localiser la couche suspecte, collecter des preuves minimales, interpréter ces preuves, puis décider d’une action prudente. Le support ne propose pas de modification destructive par défaut. Toute action de changement, de patching, de redémarrage, de mise hors ligne ou de suppression doit être traitée dans un runbook validé et explicitement signalée comme risquée.

    Pour ce module, l’analyse doit rester spécifique à **ASM et modèle de stockage**. Les preuves attendues ne sont pas un simple inventaire système ; elles doivent démontrer la compréhension du mécanisme Exadata concerné, de ses dépendances et de ses limites.

    ## Commandes et vues utiles en lecture

    Les commandes suivantes sont fournies comme exemples de lecture. Elles doivent être adaptées à la version, aux privilèges et aux standards de l’environnement. Les commandes nécessitant des privilèges élevés sont indiquées en commentaire lorsqu’elles peuvent varier selon site.

    ```bash
    asmcmd lsdg
asmcmd lsdsk -k -G DATA
select group_number,name,type,total_mb,free_mb,usable_file_mb from v$asm_diskgroup;
select name,path,failgroup,mount_status,mode_status,state from v$asm_disk;
    ```

    ## Métriques à analyser

    | Métrique ou preuve | Interprétation prudente |
    |---|---|
    | usable_file_mb | À comparer avec la période, le workload et la couche concernée ; aucun seuil universel n’est inventé dans ce support. |
| free_mb | À comparer avec la période, le workload et la couche concernée ; aucun seuil universel n’est inventé dans ce support. |
| rebalance active | À comparer avec la période, le workload et la couche concernée ; aucun seuil universel n’est inventé dans ce support. |
| disk state | À comparer avec la période, le workload et la couche concernée ; aucun seuil universel n’est inventé dans ce support. |
| failure group distribution | À comparer avec la période, le workload et la couche concernée ; aucun seuil universel n’est inventé dans ce support. |

    ## Exemple d’analyse

    **Symptôme.** Une baisse de capacité utilisable peut venir d’un disque absent, d’un rebalance en cours ou d’un déséquilibre. On vérifie ASM avant cell actions.

    **Couche suspecte.** La couche doit être choisie à partir du symptôme : base, ASM, storage cell, réseau, monitoring, sauvegarde, support ou cloud. L’analyse ne doit pas supposer la cause avant collecte.

    **Preuves à collecter.** Les preuves minimales sont les commandes et vues listées plus haut, complétées par l’heure de début, l’impact métier, le périmètre touché et l’état avant/après si disponible.

    **Interprétation.** Les résultats sont comparés avec un état de référence connu, une période équivalente ou les recommandations Oracle applicables. Le support évite d’inventer des seuils universels.

    **Prochaine action prudente.** Si l’action dépasse la lecture, produire un runbook, obtenir validation CAB ou support, et documenter rollback, impact et communication.

    ## Erreurs fréquentes

    | Erreur spécifique | Correction recommandée |
    |---|---|
    | interpréter free_mb sans usable_file_mb | Produire une preuve, relire le runbook et escalader si l’action dépasse la lecture. |
| ignorer rebalance | Produire une preuve, relire le runbook et escalader si l’action dépasse la lecture. |
| ne pas relier path ASM à griddisk | Produire une preuve, relire le runbook et escalader si l’action dépasse la lecture. |

    ## Bonnes pratiques

    | Bonne pratique | Mise en œuvre |
    |---|---|
    | documenter mapping ASM-grid disk | À intégrer dans le livrable du module. |
| surveiller rebalance avant maintenance | À intégrer dans le livrable du module. |
| éviter toute commande drop sans runbook | À intégrer dans le livrable du module. |

    ## Mini-lab ciblé

    **Objectif.** Produire le mapping ASM diskgroup vers grid disks et détecter les informations nécessaires à une maintenance prudente.

    **Étapes.** L’apprenant prépare un dossier de travail, exécute uniquement les commandes read-only adaptées à son environnement, capture les sorties horodatées, interprète les métriques propres au module et rédige une conclusion. Aucune commande de suppression, redémarrage, patching, offline/drop ou modification de paramètre n’est autorisée dans ce mini-lab.

    **Résultat attendu.** Le résultat doit relier un symptôme ou un objectif pédagogique à des preuves Exadata spécifiques, et non à un simple inventaire générique.

    ## Questions de validation

    1. Pourquoi usable_file_mb diffère-t-il de free_mb ?
2. Quel risque si un grid disk est indisponible ?

    ## Livrables attendus

    Tableau ASM/grid disk/failure group.


## Diagrammes associés

- [`physical-cell-grid-asm.mmd`](../diagrams/physical-cell-grid-asm.mmd)

## Références officielles

Les références ci-dessous doivent être utilisées comme point d'entrée, puis ajustées selon la génération Exadata, la version Oracle Database et le modèle de service utilisé.

| Référence | Usage |
|---|---|
| [Oracle University — Exadata Database Machine Administration Workshop](https://education.oracle.com/exadata-database-machine-administration-workshop/courP_4599) | Alignement pédagogique du workshop. |
| [Oracle Exadata System Software Documentation](https://docs.oracle.com/en/engineered-systems/exadata-database-machine/) | Administration Exadata, Storage Server, outils et maintenance. |
| [Oracle Maximum Availability Architecture](https://www.oracle.com/database/technologies/high-availability/maa.html) | HA/DR, Data Guard, sauvegarde, meilleures pratiques. |
| [Oracle Database Backup and Recovery User's Guide](https://docs.oracle.com/en/database/) | RMAN, restauration, récupération et validation. |
| [Oracle Autonomous Health Framework](https://docs.oracle.com/en/engineered-systems/health-diagnostics/autonomous-health-framework/) | AHF, ORAchk, Exachk et TFA. |

