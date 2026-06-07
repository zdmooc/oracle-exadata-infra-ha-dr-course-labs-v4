# Stratégie V5 — finition expert Exadata

La V5 conserve l’arborescence et les modules de la V4. Elle n’ajoute pas une nouvelle architecture de dépôt et ne remplace pas les labs existants. L’intervention cible les modules prioritaires indiqués par l’utilisateur et ajoute, dans chaque fichier concerné, un complément expert spécifique au sujet du module. Ce complément contient une explication technique approfondie, un schéma Mermaid, un exemple concret, une méthode de raisonnement, des commandes ou vues read-only, une méthode d’interprétation, un exercice, un corrigé détaillé, des limites et pièges, ainsi que des points à retenir.

Les expressions génériques explicitement signalées sont supprimées ou réduites dans les modules prioritaires. Elles ne sont pas utilisées comme substitut à l’explication technique. À la place, chaque module reçoit du vocabulaire et des mécanismes propres à Exadata : storage cells, offload, Smart Scan, IORM, ASM, failure groups, alertes cell, métriques Enterprise Manager, réseau RoCE/InfiniBand, RMAN, Data Guard, patching, ASR/SRDC, Exadata Cloud Service et Cloud@Customer.

| Axe V5 | Décision appliquée |
|---|---|
| Arborescence | Conservée strictement. |
| Modules prioritaires | 19 modules renforcés. |
| Structure V4 | Conservée, enrichie par des sections expert internes aux modules. |
| Contenu générique | Suppression des phrases répétitives ciblées. |
| Sécurité | Commandes read-only uniquement dans les ajouts. |
| Niveau pédagogique | Explications mécanistiques, sorties réalistes, exercices corrigés argumentés. |

Le dépôt tiers `https://github.com/zdmooc/oracle-infra-architecture-ha-dr-labs` reste séparé et n’est pas modifié. Il peut seulement être cité comme complément.
