    # Lab 17 — Bulk Data Loading plan

    ## Objectif

    Comparer DBFS, external tables, SQL Loader, Data Pump, direct path et rollback. Ce lab est conçu pour produire une preuve exploitable, spécifique Exadata, en privilégiant les commandes de lecture et les requêtes `SELECT`.

    ## Prérequis

    L’apprenant doit disposer d’un accès de lecture adapté au périmètre du lab, connaître le nom de la base ou du cluster si nécessaire, et avoir identifié si l’environnement est on-premises, Exadata Database Service ou Cloud@Customer. Les commandes nécessitant des privilèges élevés doivent être exécutées uniquement par un administrateur autorisé.

    ## Contexte

    Le contexte est celui d’une équipe exploitation ou support qui doit documenter l’état d’un composant Exadata sans provoquer de changement. Le lab exige une conclusion argumentée, pas seulement une copie de sorties terminal.

    ## Risques et précautions

    | Risque | Précaution |
    |---|---|
    | Exécuter une commande de changement par erreur | Se limiter aux commandes listées et lire la documentation locale. |
    | Exposer des secrets dans les logs | Masquer noms sensibles, chemins internes, OCID ou informations client avant partage. |
    | Interpréter sans contexte | Ajouter heure, hôte, rôle, version, symptôme et impact. |

    ## Étapes

    | Étape | Action | Preuve attendue |
    |---|---|---|
    | 1 | Définir périmètre, hôtes, base, cells et période. | Fiche contexte. |
    | 2 | Exécuter les commandes read-only adaptées. | Sorties horodatées. |
    | 3 | Identifier métriques ou états significatifs. | Tableau d’analyse. |
    | 4 | Rédiger conclusion prudente et prochaine action. | Livrable final. |

    ## Commandes indicatives

    ```bash
    select * from dba_external_tables;
select owner,index_name,status from dba_indexes where table_name=&TABLE;
    ```

    ## Résultat attendu

    Le résultat attendu est un document clair qui distingue faits observés, hypothèses, risques, actions recommandées et limites de l’analyse. Aucun chiffre de capacité ou de performance n’est inventé.

    ## Questions de validation

    1. Quelle couche Exadata est principalement couverte par ce lab ?
    2. Quelles preuves sont suffisantes pour soutenir la conclusion ?
    3. Quelle action serait risquée et doit être traitée dans un runbook séparé ?

    ## Livrable à produire

    `bulk-data-loading-plan.md` avec contexte, commandes, résultats, interprétation, risques, recommandations et annexes.

    ## Nettoyage / retour arrière si applicable

    Aucun nettoyage technique n’est requis car le lab est read-only. Supprimer uniquement les copies locales contenant des informations sensibles ou les anonymiser avant partage.
