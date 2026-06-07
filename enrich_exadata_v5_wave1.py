from pathlib import Path
import re

ROOT = Path('/home/ubuntu/oracle-exadata-infra-ha-dr-course-labs-v4')
MOD = ROOT / 'modules'

GENERIC_PATTERNS = [
    'Dans Exadata, une décision prise sur une couche se répercute souvent sur les autres',
    'Le fonctionnement réel peut être résumé en trois niveaux',
    'Une bonne lecture technique consiste à comprendre le chemin',
    'Les commandes doivent être adaptées au contexte',
    'La recommandation finale doit rester proportionnée',
    'IORM fait partie d’un ensemble Exadata intégré.',
    'fait partie d’un ensemble Exadata intégré',
]

def clean_text(txt: str) -> str:
    for pat in GENERIC_PATTERNS:
        txt = txt.replace(pat, '')
    txt = re.sub(r'\n{4,}', '\n\n\n', txt)
    return txt.rstrip() + '\n'

def upsert_block(filename: str, block: str):
    p = MOD / filename
    txt = clean_text(p.read_text(encoding='utf-8'))
    marker = '## Complément expert V5'
    if marker in txt:
        txt = txt.split(marker)[0].rstrip() + '\n\n'
    p.write_text(txt + block.strip() + '\n', encoding='utf-8')

blocks = {}

blocks['02-architecture.md'] = r'''
## Complément expert V5 — Architecture Exadata de bout en bout

### Explication technique spécifique

Oracle Exadata Database Machine est une plate-forme intégrée pour bases Oracle qui associe **database servers**, **storage servers**, réseau interne à faible latence, Oracle Grid Infrastructure, ASM, Exadata System Software et outils d’administration. La différence fondamentale avec une architecture Oracle classique ne tient pas seulement à la puissance des serveurs. Dans une architecture classique, la base lit des blocs depuis un SAN ou un NAS, puis filtre, joint et agrège les données côté moteur SQL. Dans Exadata, une partie du travail est déplacée vers les **storage cells** : les cellules peuvent appliquer des prédicats, projeter des colonnes, éliminer des régions de stockage et retourner un volume réduit de données vers les database servers. C’est cette coopération entre moteur SQL, ASM, protocole iDB et cellules qui donne à Exadata son caractère d’appliance intégrée.[^v5-exadata-overview]

Les **database servers** hébergent les instances Oracle RAC ou single instance, les processus foreground/background, le cache buffer, le shared pool, les processus ASM et Clusterware. Les **storage cells** hébergent Exadata System Software, présentent des grid disks à ASM, gèrent les disques physiques, les périphériques flash, les métriques cellule et les fonctions d’offload. Le réseau client expose les services SQL aux applications. Le réseau d’administration sert au pilotage, à la supervision et aux opérations d’infrastructure. Le réseau de backup transporte généralement les flux RMAN vers les appliances ou serveurs de sauvegarde. L’interconnect RoCE ou InfiniBand transporte le trafic RAC, ASM et iDB ; il conditionne directement la latence entre les instances et les cellules.

| Couche | Architecture Oracle classique | Exadata |
|---|---|---|
| Calcul SQL | Serveurs Oracle lisant des blocs depuis stockage externe | Database servers RAC coopérant avec storage cells |
| Stockage | SAN/NAS exposant LUN ou volumes | Cell disks, grid disks et ASM diskgroups pilotés par Exadata System Software |
| Filtrage | Majoritairement côté instance Oracle | Offload possible côté cellule avec Smart Scan |
| Réseau interne | Fibre Channel, Ethernet ou fabric SAN séparé | RoCE ou InfiniBand pour RAC, ASM et iDB |
| Supervision | Outils base + stockage souvent séparés | Enterprise Manager, cellcli, métriques Exadata et alertes cellule |
| Résilience | Dépend fortement du design SAN et du cluster | Redondance ASM, failure groups, cellules multiples, MAA et automatisation support |

Le chemin d’une requête SQL commence par le client, traverse le listener, atteint une instance sur un database server, est optimisé par le moteur SQL, puis accède aux segments via ASM. Si les conditions sont réunies, l’accès aux blocs est transformé en requêtes iDB vers les storage cells. Les cellules lisent disques et flash, appliquent les opérations offloadables, puis renvoient des lignes ou colonnes filtrées. Le chemin d’une I/O non offloadable est plus proche d’une lecture de blocs classique : l’instance demande des extents ASM et reçoit des blocs à traiter côté database server. Le chemin d’un backup RMAN lit les datafiles via ASM, écrit vers RECO, un média manager ou un réseau de backup. Le chemin d’une alerte naît souvent dans une cellule, un serveur, un switch ou un composant logiciel, puis remonte vers Exadata System Software, Enterprise Manager, ASR ou les journaux de diagnostic.

```mermaid
flowchart LR
    C[Client applicatif] --> L[Listener SCAN ou local]
    L --> DB[Database Server RAC]
    DB --> GI[Grid Infrastructure et ASM]
    GI --> IDB[Protocole iDB sur RoCE ou InfiniBand]
    IDB --> CELL[Storage Cell]
    CELL --> FLASH[Flash Cache et Flash Log]
    CELL --> DISK[Disques physiques]
    CELL --> ALERT[Alertes cellule]
    DB --> RMAN[RMAN]
    RMAN --> BCK[Réseau ou cible backup]
```

### Exemple concret réaliste

Une requête analytique lit une table de ventes partitionnée sur plusieurs années avec un prédicat sur `sales_date` et `region_id`. Sur SAN classique, la base peut devoir lire un grand nombre de blocs, les transférer au database server, puis filtrer. Sur Exadata, si le plan utilise un full scan direct path et si les prédicats sont offloadables, les storage cells peuvent éliminer des lignes et ne renvoyer que les colonnes utiles. Une statistique SQL Monitor typique montrera alors une différence entre **cell physical IO bytes eligible for predicate offload**, **cell physical IO interconnect bytes** et **physical read bytes**. Si l’interconnect reçoit beaucoup moins d’octets que les cellules n’en lisent, le gain provient de l’offload et non d’un simple cache.

### Comment raisonner

Pour analyser une architecture Exadata, il faut suivre les flux et non seulement lister les composants. Une question SQL se raisonne en quatre chemins : le chemin client vers l’instance, le chemin instance vers ASM, le chemin ASM/iDB vers les cellules et le chemin retour des données filtrées. Une question de disponibilité se raisonne par domaine de panne : database server, cellule, switch, disque, flash, power distribution unit, réseau client ou réseau d’administration. Une question de performance se raisonne par réduction des données transférées, latence interconnect, efficacité flash, concurrence I/O et placement ASM.

### Commandes / vues utiles

```bash
# Read-only : inventaire cellule et métriques principales
cellcli -e "list cell detail"
cellcli -e "list griddisk attributes name,asmmodestatus,asmdeactivationoutcome,size"
cellcli -e "list metriccurrent where objectType = 'CELL' attributes name,metricValue"

# Read-only : vision ASM
asmcmd lsdg
asmcmd lsdsk -p
```

```sql
-- Read-only : repérer services, instances et environnement RAC
select inst_id, instance_name, host_name, status from gv$instance order by inst_id;
select name, value from v$parameter where name in ('cluster_database','db_unique_name');
select name, total_mb, free_mb, type, state from v$asm_diskgroup order by name;
```

### Comment interpréter

Une architecture Exadata saine se reconnaît par la cohérence entre les couches. Les diskgroups ASM doivent voir les grid disks attendus, les cellules doivent être en état normal, les chemins réseau ne doivent pas montrer d’erreurs persistantes, et les plans SQL candidats doivent produire des métriques d’offload lorsqu’ils remplissent les conditions. Un manque d’offload sur une requête n’est pas automatiquement une anomalie : index access, fonctions non offloadables, types de données, chiffrement, statistiques ou choix de plan peuvent expliquer que le moteur reste côté database server.

### Exercice pratique

Explique pourquoi Exadata réduit certaines I/O par rapport à une architecture SAN classique. Construis une réponse qui distingue la quantité lue sur disque, la quantité transférée sur l’interconnect et la quantité réellement consommée par le moteur SQL.

### Corrigé détaillé

Exadata ne réduit pas toutes les I/O de façon magique. Il réduit certaines I/O **vues par le database server** parce que les storage cells peuvent exécuter une partie du travail au plus près des données. Si une table scan est éligible au Smart Scan, les cellules lisent les extents ASM, appliquent les prédicats offloadables et renvoient uniquement les lignes et colonnes nécessaires. Le disque ou la flash peut donc lire un volume important, mais l’interconnect transporte un volume inférieur. Dans une architecture SAN classique, le SAN renvoie principalement des blocs ; le database server doit ensuite filtrer. La bonne réponse doit donc distinguer les bytes lus physiquement, les bytes éligibles à l’offload et les bytes renvoyés sur l’interconnect. La réduction provient de l’intelligence des cellules, du protocole iDB, du stockage ASM distribué et des optimisations Exadata System Software, pas seulement de disques plus rapides.

### Limites et pièges

Le piège le plus courant consiste à attribuer toute amélioration à Smart Scan. Une requête peut être rapide parce que les données sont dans Flash Cache, parce que le plan utilise un index sélectif, parce que la partition pruning fonctionne ou parce que le jeu de données est déjà en cache. À l’inverse, une requête peut ne pas offloader malgré Exadata si elle utilise des fonctions non éligibles, des accès indexés très sélectifs ou des opérations qui imposent un traitement côté instance. L’architecture doit donc être lue avec SQL Monitor, les statistiques cellule, ASM et les métriques réseau.

### À retenir

Exadata est une architecture coopérative. Les database servers exécutent SQL et RAC, les storage cells exécutent stockage et offload, ASM orchestre les extents et les diskgroups, et le réseau interne relie ces couches. Apprendre Exadata consiste à comprendre les chemins réels d’une requête, d’une I/O, d’un backup et d’une alerte.

[^v5-exadata-overview]: Oracle, *Oracle Exadata Database Machine System Overview*, https://docs.oracle.com/en/engineered-systems/exadata-database-machine/
'''

blocks['06-exadata-storage-server-configuration.md'] = r'''
## Complément expert V5 — Chaîne stockage cellule, disques et grid disks

### Explication technique spécifique

Une storage cell Exadata n’expose pas directement les disques physiques aux bases de données. Elle transforme les ressources matérielles en objets administrables : **physical disks** pour les disques réels, **flash devices** pour les cartes ou modules flash, **cell disks** comme abstraction locale créée sur ces périphériques, puis **grid disks** comme unités présentées à ASM. Cette chaîne explique pourquoi ASM ne voit pas les disques physiques : ASM consomme des grid disks publiés par les cellules, ce qui permet à Exadata System Software de gérer flash cache, métriques, alertes, offload et maintenance cellule avant que la couche ASM ne voie le stockage.[^v5-cell-admin]

Un **cell disk** correspond à une portion de disque ou de flash contrôlée par la cellule. Un **grid disk** est découpé dans un cell disk et affecté à un usage logique, souvent DATA, RECO ou DBFS. Les griddisks DATA hébergent les datafiles et tempfiles via ASM ; RECO héberge souvent fast recovery area, archivelogs et backups locaux ; DBFS peut porter des usages spécifiques comme staging ou fichiers partagés selon design. Les sparse diskgroups ajoutent une capacité de provisioning optimisée pour clones ou snapshots, mais ils exigent une discipline stricte car une saturation logique peut avoir des effets rapides.

```mermaid
flowchart TD
    PD[Physical Disk] --> CD[Cell Disk]
    FD[Flash Device] --> FCD[Flash Cell Disk]
    CD --> GD1[Grid Disk DATA]
    CD --> GD2[Grid Disk RECO]
    CD --> GD3[Grid Disk DBFS]
    FCD --> FGD[Flash Grid Disk]
    GD1 --> ASM1[ASM Disk DATA]
    GD2 --> ASM2[ASM Disk RECO]
    GD3 --> ASM3[ASM Disk DBFS]
    ASM1 --> DG1[ASM Diskgroup]
    DG1 --> FILES[Datafile, tempfile, redo, archivelog]
```

### Exemple concret réaliste

Une cellule `cel01` contient douze disques haute capacité. Chaque disque est visible comme physical disk. Après configuration, la cellule crée des cell disks, puis des grid disks `DATA_CD_00_cel01`, `RECO_CD_00_cel01` et éventuellement `DBFS_CD_00_cel01`. ASM voit ces grid disks comme disques ASM, répartis dans des failure groups par cellule. Si un disque physique tombe en panne, la cellule marque les objets dépendants en erreur et ASM s’appuie sur la redondance du diskgroup pour maintenir l’accès aux fichiers. Si une cellule entière devient indisponible, tous les grid disks de son failure group disparaissent temporairement ; la capacité à survivre dépend du niveau de redondance ASM et de la distribution des extents.

### Comment raisonner

Le diagnostic stockage Exadata suit la chaîne physique vers logique. On commence par vérifier les physical disks et flash devices, puis les cell disks, puis les grid disks, puis l’état ASM. Si ASM signale un disque absent mais que la cellule voit le disque physique en bon état, l’anomalie peut être au niveau griddisk, permissions ASM, état de présentation ou communication. Si la cellule signale un predictive failure sur un disque, ASM peut encore être online grâce au mirroring ; il ne faut pas confondre survie logique et absence de risque matériel.

### Commandes / vues utiles

```bash
# Read-only : chaîne cellule complète
cellcli -e "list physicaldisk detail"
cellcli -e "list flashcache detail"
cellcli -e "list celldisk detail"
cellcli -e "list griddisk detail"
cellcli -e "list alerthistory attributes name,alertMessage,severity,beginTime"

# Read-only : vision ASM depuis Grid Infrastructure
asmcmd lsdg
asmcmd lsdsk -p
asmcmd lsdsk -k
```

```sql
-- Read-only : correspondance ASM et état des disques
select group_number, name, type, state, total_mb, free_mb from v$asm_diskgroup order by name;
select group_number, disk_number, name, path, mount_status, header_status, mode_status, state from v$asm_disk order by group_number, disk_number;
```

### Comment interpréter

`list physicaldisk detail` répond à la question matérielle : le disque ou la flash existe-t-il et dans quel état matériel se trouve-t-il ? `list celldisk detail` répond à la question d’abstraction locale : la cellule a-t-elle correctement créé et exposé sa couche interne ? `list griddisk detail` répond à la question de présentation à ASM : les objets logiques sont-ils actifs, synchrones et associés au bon usage ? `asmcmd lsdg` répond à la question base : les diskgroups disposent-ils de capacité et de redondance suffisantes ? Une divergence entre ces niveaux est souvent le point de départ du diagnostic.

### Exercice pratique

On observe qu’un diskgroup ASM DATA reste monté, mais `cellcli` signale un disque physique en predictive failure sur une cellule. Explique pourquoi la base peut continuer à fonctionner et quelles vérifications read-only effectuer avant toute action corrective.

### Corrigé détaillé

La base peut continuer à fonctionner parce qu’ASM ne dépend pas d’un seul disque physique ; il s’appuie sur des extents répartis et miroités entre failure groups. Si le diskgroup est en normal redundancy ou high redundancy, la perte d’un disque peut être absorbée tant que les copies nécessaires restent accessibles sur d’autres failure groups. Il faut vérifier l’état du physical disk, le statut des cell disks et grid disks associés, l’état ASM des disques, la capacité libre et l’existence d’alertes. Les commandes read-only pertinentes sont `cellcli -e "list physicaldisk detail"`, `cellcli -e "list celldisk detail"`, `cellcli -e "list griddisk detail"`, `asmcmd lsdg` et une requête sur `v$asm_disk`. Le corrigé est correct parce qu’il sépare le symptôme matériel de la disponibilité logique assurée par ASM.

### Limites et pièges

Ne jamais interpréter `free_mb` ASM comme capacité immédiatement utilisable sans tenir compte de la redondance, du rebalance et du niveau de failure group. Ne pas confondre un disque ASM visible avec un disque physique sain. Ne pas exécuter de commandes de drop, recreate ou alter diskgroup dans un support pédagogique sans procédure Oracle validée. La V5 conserve donc uniquement des commandes de lecture.

### À retenir

La chaîne stockage Exadata est : physical disk ou flash device, cell disk, grid disk, ASM disk, ASM diskgroup, puis fichiers Oracle. Le diagnostic expert consiste à localiser précisément le niveau où l’état diverge.

[^v5-cell-admin]: Oracle, *Oracle Exadata System Software User's Guide — CellCLI and Storage Server Administration*, https://docs.oracle.com/en/engineered-systems/exadata-database-machine/sagug/
'''

blocks['07-asm-et-modele-de-stockage.md'] = r'''
## Complément expert V5 — ASM, failure groups et résilience Exadata

### Explication technique spécifique

ASM est la couche qui transforme les grid disks fournis par les cellules en diskgroups utilisables par Oracle Database. Dans Exadata, les failure groups correspondent généralement aux storage cells. Cette organisation est essentielle : ASM place les copies d’extents dans des failure groups distincts afin qu’une panne de disque ou de cellule ne rende pas immédiatement un fichier illisible. En normal redundancy, ASM maintient deux copies ; en high redundancy, il maintient trois copies. Le choix dépend du niveau de protection recherché, de la capacité utile attendue et du design MAA.[^v5-asm-admin]

Un diskgroup DATA porte les fichiers actifs de la base, RECO porte souvent la fast recovery area, les archivelogs, flashback logs ou backups locaux, et DBFS peut servir à des usages de fichiers partagés. Un sparse diskgroup sert à des clones ou snapshots économes en espace ; il doit être surveillé plus finement parce que la consommation réelle peut augmenter avec les écritures différentielles. Le **rebalance ASM** intervient lorsqu’un disque, grid disk ou failure group change d’état ou de capacité. Le **disk repair timer** permet d’éviter de reconstruire immédiatement des extents si une panne est temporaire ; il limite les mouvements inutiles lors d’incidents courts.

```mermaid
flowchart LR
    C1[Cellule 1 Failure Group] --> DG[Diskgroup ASM DATA]
    C2[Cellule 2 Failure Group] --> DG
    C3[Cellule 3 Failure Group] --> DG
    DG --> E1[Extent primaire]
    DG --> E2[Mirror extent autre cellule]
    DG --> DBF[Datafiles]
    DG --> TMP[Tempfiles]
    DG --> REDO[Redo logs si design applicable]
```

### Exemple concret réaliste

Un cluster Exadata dispose de trois storage cells et d’un diskgroup DATA en normal redundancy. ASM place une copie primaire d’un extent sur un grid disk de `cel01` et une copie miroir sur `cel02` ou `cel03`. Si `cel01` est indisponible, les lectures peuvent continuer via les copies miroirs. Lorsque la cellule revient avant expiration du repair timer, ASM peut resynchroniser au lieu de reconstruire l’ensemble. Si la cellule ne revient pas, ASM rééquilibre les extents sur les ressources restantes, avec une consommation d’I/O qui doit être surveillée.

### Comment raisonner

Le raisonnement ASM doit répondre à quatre questions : quel diskgroup est concerné, quel niveau de redondance est actif, quel failure group porte l’anomalie et quel impact le rebalance aura sur les workloads. Une alerte de disque n’a pas la même portée selon que le diskgroup est normal ou high redundancy, selon le nombre de cellules restantes, et selon la capacité libre. Le diagnostic ne doit pas partir d’une commande corrective ; il doit partir d’une lecture de `v$asm_diskgroup`, `v$asm_disk`, `asmcmd lsdg` et des états cellule.

### Commandes / vues utiles

```bash
# Read-only : état des diskgroups et disques ASM
asmcmd lsdg
asmcmd lsdsk -p
asmcmd lsdsk -k
asmcmd lsattr -G DATA -l
```

```sql
-- Read-only : redondance, état, chemins et opérations ASM
select name, type, state, total_mb, free_mb, required_mirror_free_mb, usable_file_mb from v$asm_diskgroup order by name;
select name, failgroup, path, mount_status, header_status, mode_status, state from v$asm_disk order by failgroup, name;
select group_number, operation, state, power, actual, sofar, est_work, est_minutes from v$asm_operation;
```

### Comment interpréter

`required_mirror_free_mb` indique la capacité à conserver la redondance après incident ; il est plus significatif que `free_mb` seul. `usable_file_mb` tient compte du mirroring et donne une vision plus réaliste de la capacité utilisable. `v$asm_operation` permet de voir si un rebalance est actif ; un rebalance prolongé peut concurrencer les workloads, surtout si la puissance est élevée ou si l’environnement est déjà saturé. Les colonnes `mount_status`, `header_status` et `mode_status` aident à distinguer un disque absent, membre, candidate ou en problème d’accès.

### Exercice pratique

Un diskgroup DATA en normal redundancy affiche `free_mb` positif mais `usable_file_mb` très faible. Explique pourquoi ajouter des datafiles peut rester risqué.

### Corrigé détaillé

`free_mb` mesure l’espace brut libre dans le diskgroup. En normal redundancy, chaque extent doit être miroité dans un autre failure group ; l’espace réellement utilisable dépend donc de la capacité à placer les copies tout en respectant les règles de mirroring. `usable_file_mb` intègre cette contrainte et peut devenir faible alors que `free_mb` semble encore confortable. Ajouter des datafiles sur la base de `free_mb` seul peut provoquer une pression de capacité ou empêcher ASM de maintenir la redondance après panne. La réponse correcte cite donc `required_mirror_free_mb`, `usable_file_mb`, le niveau de redondance et la distribution entre failure groups.

### Limites et pièges

Ne pas conclure qu’un diskgroup est sain parce qu’il est monté. Un diskgroup peut être monté tout en ayant une marge de redondance insuffisante, un rebalance en cours ou des disques en état dégradé. Ne pas interpréter les sparse diskgroups comme de la capacité gratuite. Ne pas modifier la puissance de rebalance sans tenir compte de la fenêtre de charge.

### À retenir

ASM est la couche de résilience logique d’Exadata. Comprendre DATA, RECO, DBFS, sparse, failure groups, mirroring, repair timer et rebalance est indispensable pour diagnostiquer une panne de disque ou de cellule.

[^v5-asm-admin]: Oracle, *Oracle Automatic Storage Management Administrator's Guide*, https://docs.oracle.com/en/database/oracle/oracle-database/19/ostmg/
'''

blocks['08-iorm.md'] = r'''
## Complément expert V5 — IORM comme gouverneur d’I/O côté storage cells

### Explication technique spécifique

IORM agit dans les **storage cells** pour arbitrer l’accès aux ressources I/O entre plusieurs bases, pluggable databases ou catégories de workloads. Il ne remplace pas Database Resource Manager : DBRM classe et gouverne les sessions côté base, alors qu’IORM protège l’accès au stockage partagé côté cellules. Dans une consolidation Exadata, IORM évite qu’un batch volumineux, un reporting non prioritaire ou une opération de maintenance monopolise les I/O au détriment d’une base OLTP critique. La décision est appliquée près du stockage, là où les requêtes iDB concurrentes arrivent depuis les database servers.[^v5-iorm]

IORM peut utiliser des plans orientés base de données, catégories ou objectifs. Les paramètres définissent des allocations, limites ou priorités ; la cellule mesure ensuite la demande réelle et arbitre. Cela ne transforme pas un workload mal conçu en workload rapide, mais cela évite qu’un consommateur agressif dégrade tout l’environnement. L’intérêt est maximal dans les environnements consolidés, RAC multi-bases ou Cloud@Customer où plusieurs équipes partagent les mêmes cellules.

```mermaid
flowchart TD
    DB1[Base OLTP critique] --> IDB1[Requêtes iDB]
    DB2[Reporting décisionnel] --> IDB2[Requêtes iDB]
    DB3[Batch chargement] --> IDB3[Requêtes iDB]
    IDB1 --> CELL[IORM dans les storage cells]
    IDB2 --> CELL
    IDB3 --> CELL
    CELL --> FLASH[Flash]
    CELL --> DISK[Disques]
    CELL --> POLICY[Priorités, allocations, limites]
```

### Exemple concret réaliste

Une plate-forme héberge `CRMPRD`, `DWPRD` et `TESTLOAD`. Sans IORM, un chargement massif sur `TESTLOAD` peut provoquer une file d’attente I/O qui augmente la latence des lectures critiques de `CRMPRD`. Avec un plan IORM, `CRMPRD` reçoit une priorité ou une allocation minimale supérieure ; `TESTLOAD` reste autorisée mais ne peut pas consommer toute la bande passante cellule. Le DBA observe alors que les temps d’attente `cell single block physical read` et `cell smart table scan` de `CRMPRD` restent contenus pendant le batch.

### Comment raisonner

Le raisonnement IORM commence par identifier la concurrence réelle. Si une seule base utilise Exadata, IORM ne créera pas un gain spectaculaire. Si plusieurs bases ou services se disputent flash et disques, il faut classer les workloads par criticité métier, variabilité, fenêtre horaire et tolérance à la latence. Ensuite, on vérifie que les plans DBRM côté base et IORM côté cellule expriment la même intention. Une politique incohérente peut prioriser une session côté base mais la ralentir côté stockage, ou inversement.

### Commandes / vues utiles

```bash
# Read-only : configuration et métriques IORM
cellcli -e "list iormplan detail"
cellcli -e "list metriccurrent where name like 'IORM%' attributes name,metricValue,objectName"
cellcli -e "list metrichistory where name like 'IORM%' attributes name,metricValue,collectionTime"
```

```sql
-- Read-only : waits et consommation par base ou service
select inst_id, event, total_waits, time_waited_micro from gv$system_event where event like 'cell%' order by time_waited_micro desc fetch first 20 rows only;
select inst_id, name, value from gv$sysstat where name like 'cell%IO%' order by inst_id, name;
```

### Comment interpréter

Une latence élevée sur des événements `cell%` ne prouve pas seule un problème IORM. Il faut corréler le moment, la concurrence, les métriques cellule et le plan actif. Si les métriques montrent qu’un workload limité atteint régulièrement son plafond alors que la base prioritaire reste stable, IORM fonctionne. Si toutes les bases souffrent en même temps, le problème peut être une saturation physique, un rebalance ASM, un patching, un défaut réseau ou une erreur de design de plan.

### Exercice pratique

Dans une consolidation, une base de reporting dégrade la base OLTP pendant la clôture mensuelle. Propose un raisonnement pour décider si IORM doit être utilisé et explique ce que tu vérifierais avant de modifier un plan.

### Corrigé détaillé

Il faut d’abord prouver la concurrence sur les cellules : mêmes fenêtres horaires, hausse des waits `cell smart table scan` ou `cell single block physical read`, augmentation de la latence I/O et activité importante de la base de reporting. Ensuite, il faut identifier la criticité : l’OLTP doit conserver une latence basse, le reporting peut accepter un débit plus faible. IORM est pertinent parce que le conflit se produit côté stockage partagé. Avant modification, on lit le plan actif avec `cellcli -e "list iormplan detail"`, les métriques IORM, les waits côté base et les services impliqués. Le corrigé est correct car il ne prescrit pas une politique arbitraire ; il établit le lien entre concurrence observable, objectif métier et gouvernance cellule.

### Limites et pièges

IORM ne corrige pas un SQL non sélectif, un mauvais partitionnement ou un manque de statistiques. Il ne remplace pas DBRM, qui reste nécessaire pour classer les sessions et limiter CPU ou parallelisme côté base. Un plan trop agressif peut ralentir des traitements nécessaires comme backups, chargements ou maintenance. Il faut donc tester en fenêtre contrôlée et surveiller les effets sur toutes les bases.

### À retenir

IORM est l’outil de justice I/O d’Exadata. Il protège les workloads critiques dans les cellules, surtout lorsque plusieurs bases partagent le même stockage.

[^v5-iorm]: Oracle, *Managing I/O Resources with IORM*, https://docs.oracle.com/en/engineered-systems/exadata-database-machine/sagug/managing-io-resources.html
'''

blocks['10-smart-scan.md'] = r'''
## Complément expert V5 — Smart Scan, offload et réduction du trafic interconnect

### Explication technique spécifique

Smart Scan est le mécanisme par lequel Exadata déporte certaines opérations vers les storage cells. Lorsqu’un plan effectue un accès compatible, souvent un full table scan ou fast full scan en direct path, la cellule peut filtrer des lignes, projeter des colonnes, appliquer Storage Index, traiter certaines fonctions et réduire les données renvoyées. Le database server ne reçoit plus nécessairement tous les blocs ; il reçoit un résultat partiel déjà réduit. Les statistiques `cell physical IO bytes eligible for predicate offload`, `cell physical IO interconnect bytes` et `cell physical IO bytes saved by storage index` permettent d’observer ce comportement.[^v5-smart-scan]

Smart Scan n’est pas déclenché par le simple fait d’être sur Exadata. Il dépend du plan, du type d’accès, des prédicats, du format des segments, de la compression, du parallélisme, du cache et des opérations SQL. Un index range scan très sélectif peut être meilleur qu’un Smart Scan. À l’inverse, une requête analytique sur une grande table peut être beaucoup plus efficace si les cellules éliminent les données avant transfert.

```mermaid
sequenceDiagram
    participant SQL as Moteur SQL
    participant ASM as ASM / iDB
    participant CELL as Storage Cell
    participant DISK as Flash / Disques
    SQL->>ASM: Demande scan segment
    ASM->>CELL: Requête iDB avec prédicats offloadables
    CELL->>DISK: Lecture extents
    CELL->>CELL: Filtrage, projection, Storage Index
    CELL-->>SQL: Résultat réduit sur interconnect
```

### Exemple concret réaliste

Une table `SALES` contient 2 To. La requête demande `sum(amount)` pour une région et un mois. Si le plan effectue un full scan direct path et que les prédicats sur `sale_month` et `region_id` sont offloadables, les cellules peuvent lire un volume élevé mais renvoyer peu d’octets. Dans SQL Monitor, on peut voir une activité cellule importante et un trafic interconnect réduit. Si la même requête utilise une fonction non offloadable sur la colonne filtrée, le moteur peut devoir recevoir plus de données et filtrer côté database server.

### Comment raisonner

Le raisonnement Smart Scan suit une séquence : vérifier le plan d’exécution, confirmer que l’accès est compatible, vérifier les statistiques d’offload, comparer octets lus et octets interconnect, puis examiner les prédicats. Si les bytes éligibles sont élevés mais les bytes interconnect ne diminuent pas, les prédicats ne filtrent peut-être pas beaucoup. Si les bytes éligibles sont faibles, le plan ne déclenche peut-être pas l’offload. Si Storage Index économise des bytes, la localisation des valeurs dans les régions de stockage est favorable.

### Commandes / vues utiles

```sql
-- Read-only : statistiques offload sur la session courante ou historique selon contexte
select name, value from v$mystat m join v$statname n using(statistic#)
where name like 'cell physical IO%' order by name;

select * from table(dbms_xplan.display_cursor(null,null,'ALLSTATS LAST +IOSTATS +PREDICATE'));

select sql_id, plan_hash_value, elapsed_time, io_interconnect_bytes, physical_read_bytes
from v$sql where sql_text like '%SALES%' fetch first 10 rows only;
```

```bash
# Read-only : métriques cellule associées au scan et à l’I/O
cellcli -e "list metriccurrent where name like 'CL_%' attributes name,metricValue,objectName"
cellcli -e "list metriccurrent where name like 'FC_%' attributes name,metricValue,objectName"
```

### Comment interpréter

Un bon résultat Smart Scan ne signifie pas toujours baisse du temps total si le SQL est CPU-bound après agrégation ou si le parallélisme crée un goulot ailleurs. L’indicateur clé est la relation entre volume éligible, volume lu, volume renvoyé et temps d’attente. Si `io_interconnect_bytes` est proche de `physical_read_bytes`, la réduction est faible. Si `cell physical IO bytes saved by storage index` augmente, les Storage Index évitent des lectures de régions entières. L’interprétation doit donc combiner plan, statistiques et métriques cellule.

### Exercice pratique

Une requête full scan sur une grande table est lente malgré Exadata. Les statistiques montrent peu de bytes éligibles à l’offload. Donne trois causes possibles et indique comment les vérifier.

### Corrigé détaillé

Première cause : le plan n’utilise pas un accès compatible avec Smart Scan, par exemple un accès indexé ou un accès bufferisé ; on le vérifie avec `dbms_xplan.display_cursor`. Deuxième cause : les prédicats ou fonctions ne sont pas offloadables ; on lit la section predicate information du plan et on compare les statistiques cellule. Troisième cause : la requête n’effectue pas un direct path read, par exemple parce que la table est petite ou fortement mise en cache ; on vérifie les waits, les statistiques de session et le plan réel. La réponse est correcte parce qu’elle ne conclut pas que Smart Scan est cassé ; elle examine les conditions d’éligibilité.

### Limites et pièges

Smart Scan n’est pas une stratégie d’indexation. Il complète le modèle physique, la compression, la partitioning et la qualité SQL. Forcer des full scans pour obtenir l’offload peut dégrader l’OLTP. Un SQL Monitor isolé peut être trompeur si le cache, la concurrence ou le parallélisme changent entre deux exécutions.

### À retenir

Smart Scan réduit le travail remonté aux database servers lorsque le plan et les prédicats le permettent. Le diagnostic expert compare toujours les octets lus par les cellules et les octets transportés sur l’interconnect.

[^v5-smart-scan]: Oracle, *Oracle Exadata Smart Scan and Storage Server Software Concepts*, https://docs.oracle.com/en/engineered-systems/exadata-database-machine/dbmso/exadata-storage-server-software.html
'''

blocks['13-bulk-data-loading.md'] = r'''
## Complément expert V5 — Chargements massifs sur Exadata

### Explication technique spécifique

Le chargement massif sur Exadata doit concilier débit, journalisation, pression flash, impact ASM, redo, undo, statistiques et concurrence I/O. Les méthodes fréquentes sont SQL*Loader direct path, external tables, Data Pump, `insert /*+ append */`, transportable tablespaces et chargements parallèles. Exadata accélère certains flux grâce à la bande passante stockage, au parallélisme et à la flash, mais un chargement mal gouverné peut saturer RECO avec les archivelogs, provoquer des waits I/O, perturber IORM ou déclencher des rebalances si la capacité est mal anticipée.[^v5-sqlloader]

Un chargement expert sépare la phase d’ingestion, la phase de validation, la phase de statistiques et la phase de mise à disposition. Les tables de staging peuvent recevoir les données avec contraintes différées, puis les partitions peuvent être échangées vers la table cible. Pour les très gros volumes, le partition exchange load réduit la durée de verrouillage sur la table finale. La question n’est pas seulement “comment charger vite”, mais “comment charger vite sans casser la fenêtre de production ni saturer les couches Exadata”.

```mermaid
flowchart LR
    SRC[Fichiers source ou dump] --> STG[Staging table]
    STG --> VALID[Contrôles qualité]
    VALID --> PEL[Partition Exchange Load]
    PEL --> TGT[Table cible partitionnée]
    TGT --> STATS[Stats incrémentales]
    STG --> REDO[Redo / Archivelogs]
    REDO --> RECO[Diskgroup RECO]
```

### Exemple concret réaliste

Une équipe doit charger 800 Go de transactions quotidiennes dans une table partitionnée. Un chargement direct dans la table finale avec index globaux actifs peut générer beaucoup de redo et prolonger les verrous. Une approche plus robuste consiste à charger en staging avec direct path, contrôler les rejets, créer ou maintenir les index locaux, collecter les statistiques sur la partition, puis effectuer un exchange partition. Pendant l’opération, le DBA suit RECO, les waits `direct path write`, `log file sync`, les métriques cellule et la consommation CPU des database servers.

### Comment raisonner

Le raisonnement commence par le contrat de service : fenêtre disponible, volume, taux d’erreurs attendu, possibilité de rejouer, niveau de journalisation exigé et impact acceptable. Ensuite, on choisit la méthode : SQL*Loader pour fichiers plats, external tables pour SQL sur fichiers, Data Pump pour export/import Oracle, direct path insert pour transformations SQL, transportable tablespaces pour déplacement massif de segments. Enfin, on prépare la surveillance : DATA, RECO, archivelogs, parallélisme, stats et IORM.

### Commandes / vues utiles

```sql
-- Read-only : suivre sessions de chargement et waits
select sid, serial#, program, event, state, wait_class from v$session where program like '%sqlldr%' or module like '%Data Pump%';
select name, value from v$sysstat where name in ('redo size','physical writes direct','physical reads direct');
select tablespace_name, bytes/1024/1024 mb from dba_data_files fetch first 20 rows only;
select table_name, partition_name, num_rows, blocks, last_analyzed from dba_tab_partitions where table_name = 'SALES';
```

```bash
# Read-only : capacité ASM et cellule pendant chargement
asmcmd lsdg
cellcli -e "list metriccurrent where name like 'CD_IO%' attributes name,metricValue,objectName"
```

### Comment interpréter

Une hausse de `redo size` est normale si le chargement est journalisé ; elle devient problématique si RECO approche de la saturation ou si l’archivage ne suit plus. Les waits `direct path write` indiquent l’écriture directe des segments ; leur durée doit être analysée avec la charge cellule. Les index globaux peuvent transformer un chargement séquentiel en maintenance coûteuse. Les statistiques absentes après chargement peuvent produire de mauvais plans malgré un chargement réussi.

### Exercice pratique

On doit charger 800 Go en deux heures dans une table partitionnée utilisée le lendemain matin. Propose une stratégie Exadata et explique pourquoi elle limite le risque.

### Corrigé détaillé

Une stratégie robuste consiste à charger en staging avec direct path et parallélisme contrôlé, vérifier les rejets, collecter des statistiques sur les données chargées, puis utiliser partition exchange load vers la table cible. Il faut surveiller DATA, RECO, archivelogs, waits direct path et métriques cellule. Si la base est en production, IORM ou DBRM peut limiter l’impact sur les workloads critiques. Le corrigé est correct parce qu’il traite le chargement comme un processus complet : ingestion, validation, bascule, statistiques et surveillance, au lieu de se limiter à une commande rapide.

### Limites et pièges

Le mode NOLOGGING peut être tentant mais il a des implications de récupération et de Data Guard ; il doit respecter les règles de protection de l’entreprise. Un parallélisme trop élevé peut saturer CPU, I/O ou redo. Un exchange partition sans statistiques peut créer une régression le lendemain. Un chargement réussi techniquement mais non contrôlé fonctionnellement reste un échec opérationnel.

### À retenir

Sur Exadata, un chargement massif performant est un compromis maîtrisé entre débit, redo, capacité RECO, parallélisme, index, statistiques et protection des workloads concurrents.

[^v5-sqlloader]: Oracle, *Oracle Database Utilities — SQL*Loader and Data Pump*, https://docs.oracle.com/en/database/oracle/oracle-database/19/sutil/
'''

for fname, block in blocks.items():
    upsert_block(fname, block)

print(f'V5 wave1 enriched: {len(blocks)} modules')
