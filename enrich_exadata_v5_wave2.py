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
    'fait partie d’un ensemble Exadata intégré',
    'un même symptôme peut avoir plusieurs causes',
    'il faut relier la mesure au composant concerné',
    'La première étape consiste à identifier la couche concernée'
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


def monitoring_block(title, object_name, symptom, metrics, commands, exercise, correction, mermaid_nodes, source_note):
    metric_rows = '\n'.join([f'| `{m[0]}` | {m[1]} | {m[2]} |' for m in metrics])
    command_text = '\n'.join(commands)
    return f'''
## Complément expert V5 — {title}

### Explication technique spécifique

Le monitoring Exadata ne consiste pas à regarder une seule alerte ou un seul graphe. Pour **{object_name}**, l’objectif est de rapprocher l’état matériel, l’état logiciel, les métriques courantes et la perception côté base. Une alerte cellule peut être bénigne si elle correspond à une transition attendue, mais elle peut aussi expliquer une hausse de latence observée par les sessions Oracle. La démarche experte consiste à identifier la mesure native, son objet, son horodatage, puis à la comparer avec les waits, les statistiques SQL et l’état ASM. Enterprise Manager apporte une vision centralisée, tandis que `cellcli`, les vues dynamiques et les journaux de diagnostic donnent une preuve locale.[^v5-monitoring]

Pour ce thème, un DBA confirmé doit distinguer **symptôme**, **cause probable** et **preuve observable**. Le symptôme typique est : {symptom}. La cause peut être locale au composant, liée à une saturation, à une opération planifiée ou à une panne partielle. La preuve doit venir d’au moins deux sources indépendantes : métrique cellule et vue base, alerte système et historique Enterprise Manager, ou état ASM et journal Exadata.

| Indicateur | Ce qu’il mesure | Interprétation experte |
|---|---|---|
{metric_rows}

```mermaid
flowchart LR
{mermaid_nodes}
```

### Exemple concret réaliste

Pendant une fenêtre de reporting, l’équipe observe {symptom}. Le réflexe débutant serait de conclure à un problème général de performance. L’analyse V5 impose plutôt de vérifier si l’événement est isolé à une cellule, à un database server, à un réseau ou à une base. Si une seule cellule montre une métrique anormale alors que les autres restent stables, la piste est locale. Si toutes les cellules montrent la même hausse au même instant, il faut chercher une opération globale : chargement massif, backup, rebalance ASM, scan parallèle ou patching.

### Comment raisonner

Commence par fixer la période exacte de l’incident, puis compare trois horloges : heure applicative, heure base et heure composant Exadata. Ensuite, identifie l’objet affecté : cellule, disque, flash, port réseau, instance, service, diskgroup ou target Enterprise Manager. Enfin, vérifie si l’anomalie modifie réellement l’expérience des sessions : hausse des waits, baisse de débit, erreurs applicatives ou alertes critiques. Une métrique élevée sans impact observable peut rester un signal de capacité ; une métrique modérée mais corrélée à des erreurs peut être prioritaire.

### Commandes / vues utiles

```bash
{command_text}
```

```sql
select inst_id, event, total_waits, time_waited_micro
from gv$system_event
where event like 'cell%' or event like 'gc%' or event like 'log file%'
order by time_waited_micro desc fetch first 20 rows only;

select inst_id, name, value
from gv$sysstat
where name like 'cell%' or name like 'physical%'
order by inst_id, name;
```

### Comment interpréter

L’interprétation correcte cherche une corrélation, pas une coïncidence. Si la métrique change avant le symptôme applicatif, elle peut être causale. Si elle change après, elle peut être une conséquence. Si elle ne change que sur un composant, la portée est locale. Si elle change partout, la cause est probablement un workload ou une opération de plate-forme. {source_note}

### Exercice pratique

{exercise}

### Corrigé détaillé

{correction}

### Limites et pièges

Le principal piège est de diagnostiquer depuis une capture unique. Exadata est fortement parallèle : un instantané peut masquer un pic court, un effet de cache ou une opération transitoire. Il faut conserver l’horodatage, comparer plusieurs composants et éviter les actions correctives sans preuve. Les commandes proposées ici restent read-only et servent à documenter l’état, pas à modifier la plate-forme.

### À retenir

Pour {object_name}, le monitoring expert relie métriques Exadata, vues Oracle, alertes et chronologie. La valeur pédagogique vient de l’interprétation, pas de l’accumulation de sorties brutes.

[^v5-monitoring]: Oracle, *Monitoring Oracle Exadata Database Machine*, https://docs.oracle.com/en/engineered-systems/exadata-database-machine/dbmmn/
'''

blocks = {}

blocks['14-platform-monitoring-introduction.md'] = monitoring_block(
    'Introduction au monitoring Exadata multi-couches',
    'la plate-forme Exadata complète',
    'une hausse simultanée des temps de réponse SQL et des alertes de capacité',
    [('DB_IO_RQ_SM_SEC', 'Débit de petites I/O côté base ou cellule selon contexte', 'Utile pour distinguer OLTP intensif et scans volumineux'), ('CL_CPUT', 'Utilisation CPU cellule', 'Une cellule CPU-bound peut ralentir offload et compression'), ('GD_IO_RQ_LG_SEC', 'Grandes requêtes I/O sur grid disks', 'Souvent lié aux scans, backups ou chargements')],
    ['cellcli -e "list cell detail"', 'cellcli -e "list metriccurrent attributes name,metricValue,objectName"', 'cellcli -e "list alerthistory attributes severity,alertMessage,beginTime"'],
    'Un rapport EM montre une hausse globale de latence à 22h00. Décris comment distinguer incident plate-forme et batch applicatif.',
    'La bonne réponse commence par la chronologie et l’étendue. Si toutes les bases et cellules sont touchées à 22h00, un batch, backup ou rebalance global est probable. Si une seule base souffre, il faut inspecter ses plans SQL et services. On vérifie les alertes, métriques cellule, waits GV$ et jobs planifiés. La conclusion est justifiée seulement si les sources convergent.',
    '    APP[Applications] --> DB[Instances RAC]\n    DB --> ASM[ASM]\n    ASM --> CELL[Storage Cells]\n    CELL --> MET[Métriques CellCLI]\n    DB --> AWR[AWR / ASH]\n    MET --> EM[Enterprise Manager]\n    AWR --> EM',
    'Une hausse globale sans alerte matérielle oriente vers le workload ; une alerte critique localisée oriente vers composant.'
)

blocks['15-monitoring-exadata-system-software.md'] = monitoring_block(
    'Exadata System Software et services cellule',
    'Exadata System Software',
    'des alertes répétées sur une cellule et une baisse d’efficacité Smart Scan',
    [('CL_CPUT', 'CPU consommé sur la cellule', 'Peut indiquer offload, compression ou tâches internes'), ('CL_MEMUT', 'Utilisation mémoire cellule', 'À corréler avec services cellule et alertes'), ('IORM_MODE', 'Mode ou état lié à IORM selon version', 'Confirme la présence de gouvernance I/O')],
    ['cellcli -e "list cell attributes name,releaseVersion,kernelVersion,makeModel,status"', 'cellcli -e "list metriccurrent where objectType = \'CELL\' attributes name,metricValue"', 'cellcli -e "list alerthistory attributes severity,alertMessage,beginTime"'],
    'Une cellule affiche une version logicielle différente des autres après maintenance. Explique le risque pédagogique et les preuves à collecter.',
    'Il faut vérifier la version avec `list cell attributes releaseVersion`, comparer toutes les cellules, lire les alertes et vérifier les symptômes côté base. Une différence de version après maintenance peut être temporaire ou révéler un patch incomplet. La réponse correcte ne demande pas de corriger directement ; elle documente l’écart et prépare l’escalade.',
    '    CELL[Storage Cell] --> CELLSRV[cellsrv]\n    CELL --> MS[management server]\n    CELL --> RS[restart server]\n    CELLSRV --> OFF[Offload et I/O]\n    MS --> ALERT[Alertes et métriques]\n    ALERT --> EM[Enterprise Manager]',
    'Une cellule peut répondre au ping tout en ayant un service Exadata dégradé ; l’état réseau seul n’est pas suffisant.'
)

blocks['16-enterprise-manager-cloud-control.md'] = monitoring_block(
    'Enterprise Manager Cloud Control pour Exadata',
    'Enterprise Manager Cloud Control',
    'un incident visible dans EM mais difficile à reproduire en ligne de commande',
    [('Target Status', 'État agrégé d’une cible EM', 'Donne la portée mais peut masquer le composant racine'), ('Incident count', 'Nombre d’incidents ouverts', 'À qualifier par sévérité et répétition'), ('Metric collection error', 'Erreur de collecte', 'Peut indiquer un problème agent plutôt qu’un problème Exadata')],
    ['emctl status agent', 'emctl status agent scheduler', 'cellcli -e "list alerthistory attributes severity,alertMessage,beginTime"'],
    'EM signale une target Exadata down mais les bases répondent. Explique comment éviter une fausse conclusion.',
    'La target EM down peut venir d’un agent, d’un credential, d’une collecte ou d’un réseau d’administration. Il faut vérifier l’agent, l’état réel des cellules, les instances et les alertes. Si la base répond et que CellCLI ne montre pas d’erreur, l’incident porte peut-être sur la supervision, pas sur le service de données.',
    '    TARGET[Cible Exadata EM] --> AGENT[Agent EM]\n    AGENT --> CELL[Cellules]\n    AGENT --> DB[Database Targets]\n    AGENT --> HOST[Hosts]\n    TARGET --> INCIDENT[Incidents]\n    TARGET --> METRIC[Métriques historiques]',
    'EM est excellent pour la tendance et l’agrégation ; CellCLI et les vues dynamiques restent nécessaires pour la preuve locale.'
)

blocks['17-monitoring-storage-servers.md'] = monitoring_block(
    'Monitoring des storage servers',
    'les storage servers',
    'une seule cellule montre une latence I/O plus élevée que les autres',
    [('CD_IO_RQ_R_SM_SEC', 'Petites lectures par cell disk', 'Montre la pression OLTP ou metadata'), ('CD_IO_RQ_W_LG_SEC', 'Grandes écritures par cell disk', 'Peut signaler chargement, backup ou rebalance'), ('FC_BY_USED', 'Utilisation Flash Cache', 'Aide à comprendre pression flash')],
    ['cellcli -e "list cell detail"', 'cellcli -e "list celldisk attributes name,status,size,freeSpace"', 'cellcli -e "list metriccurrent where objectType = \'CELLDISK\' attributes name,metricValue,objectName"', 'cellcli -e "list physicaldisk detail"'],
    'Une cellule est plus lente que les autres pendant les scans. Donne une démarche read-only.',
    'La démarche vérifie d’abord physicaldisk et celldisk, puis métriques CELLDISK et GRIDDISK, alertes et répartition ASM. Si une cellule a un disque dégradé ou une file d’attente anormale, l’hypothèse locale est forte. Si toutes les cellules ont le même profil, la cause est probablement workload ou plan SQL.',
    '    DB[Database Servers] --> IDB[iDB]\n    IDB --> C1[Cellule 1]\n    IDB --> C2[Cellule 2]\n    IDB --> C3[Cellule 3]\n    C2 --> PD[Physical disks]\n    C2 --> FC[Flash Cache]\n    C2 --> AL[Alertes cellule]',
    'Une cellule lente n’est pas forcément en panne ; elle peut porter plus d’extents chauds ou subir un rebalance.'
)

blocks['18-monitoring-database-servers.md'] = monitoring_block(
    'Monitoring des database servers',
    'les database servers',
    'une instance RAC montre plus de waits que les autres',
    [('CPU usage', 'CPU hôte ou instance', 'Distingue saturation CPU et attente I/O'), ('gc waits', 'Attentes Global Cache', 'Indique contention RAC ou interconnect'), ('cell waits', 'Attentes liées aux cellules', 'Relie instance et stockage Exadata')],
    ['uptime', 'vmstat 1 5', 'srvctl status database -d <DB_UNIQUE_NAME>', 'olsnodes -n'],
    'Une instance RAC est lente alors que les cellules semblent normales. Quelle piste explores-tu ?',
    'Il faut vérifier CPU, mémoire, services RAC, répartition des sessions, waits `gc%`, plans SQL et réseau interconnect. Si les cellules sont normales mais une instance souffre, la cause peut être locale au database server, à un service mal réparti ou à une contention RAC.',
    '    SVC[Services applicatifs] --> I1[Instance 1]\n    SVC --> I2[Instance 2]\n    I1 --> CPU1[CPU / mémoire host]\n    I2 --> CPU2[CPU / mémoire host]\n    I1 --> GC[Global Cache]\n    I1 --> CELL[Storage Cells]',
    'Une instance lente ne prouve pas une cellule lente ; le diagnostic RAC reste indispensable.'
)

blocks['19-monitoring-network.md'] = monitoring_block(
    'Monitoring réseau client, admin, backup et interconnect',
    'les réseaux Exadata',
    'des timeouts applicatifs alors que la base et les cellules restent up',
    [('Interface errors', 'Erreurs RX/TX', 'Indique pertes ou défaut de lien'), ('gc cr block receive time', 'Temps de réception RAC', 'Sensible à l’interconnect'), ('backup throughput', 'Débit sauvegarde', 'Aide à isoler saturation réseau backup')],
    ['ip -s link', 'ip route', 'netstat -s | head -80', 'cellcli -e "list metriccurrent where name like \'N_%\' attributes name,metricValue,objectName"'],
    'Un backup RMAN ralentit mais les scans SQL restent corrects. Explique pourquoi le réseau backup devient suspect.',
    'Si les scans SQL utilisent l’interconnect interne et restent stables alors que RMAN vers cible externe ralentit, la piste réseau backup ou cible backup est plus probable que storage cell. Il faut comparer débit RMAN, erreurs interfaces, routes et charge cible.',
    '    CLIENT[Réseau client] --> DB[DB servers]\n    ADMIN[Réseau admin] --> EM[EM / SSH]\n    BACKUP[Réseau backup] --> RMAN[Flux RMAN]\n    DB --> IB[RoCE ou InfiniBand]\n    IB --> CELL[Storage Cells]',
    'Chaque réseau a une fonction différente ; mélanger les symptômes conduit à de mauvaises conclusions.'
)

blocks['20-monitoring-other-components.md'] = monitoring_block(
    'Monitoring des composants annexes : alimentation, température, switches et firmware',
    'les composants physiques annexes',
    'des alertes matérielles sans erreur SQL immédiate',
    [('Temperature', 'Température composant', 'Peut précéder throttling ou panne'), ('Power supply status', 'État alimentation', 'Critique pour redondance châssis'), ('Switch port state', 'État port switch', 'Impact possible sur interconnect ou management')],
    ['cellcli -e "list alerthistory attributes severity,alertMessage,beginTime"', 'ipmitool sensor 2>/dev/null || true', 'ipmitool sel list 2>/dev/null || true'],
    'Une alimentation redondante est en alerte mais la base fonctionne. Explique pourquoi il faut traiter l’alerte.',
    'La disponibilité immédiate ne signifie pas absence de risque. Une alimentation redondante en défaut réduit la tolérance à la prochaine panne. Il faut documenter l’alerte, vérifier le composant, l’historique et planifier le remplacement selon procédure support.',
    '    HW[Capteurs matériels] --> ALERT[Alertes]\n    ALERT --> EM[Enterprise Manager]\n    ALERT --> SR[Support]\n    HW --> RISK[Risque de perte de redondance]\n    RISK --> PLAN[Maintenance planifiée]',
    'Les composants annexes sont souvent des signaux faibles de risque, pas des causes immédiates de lenteur SQL.'
)

blocks['21-other-monitoring-tools.md'] = monitoring_block(
    'Outils complémentaires : AWR, ASH, CellCLI, OSWatcher et journaux',
    'les outils de diagnostic complémentaires',
    'des métriques contradictoires entre AWR, CellCLI et système',
    [('AWR DB Time', 'Temps base agrégé', 'Mesure impact SQL global'), ('ASH samples', 'Échantillons sessions actives', 'Localise les sessions et événements'), ('CellCLI history', 'Historique cellule', 'Relie base et stockage')],
    ['cellcli -e "list metrichistory attributes name,metricValue,collectionTime,objectName"', 'adrci exec="show alert -tail 50"', 'ls -1 $ORACLE_BASE/diag 2>/dev/null || true'],
    'AWR montre `cell smart table scan`, mais CellCLI ne montre pas d’alerte. Que conclure ?',
    'Un wait `cell smart table scan` peut être normal pour un scan offloadé. Sans alerte cellule ni latence anormale, il décrit une activité, pas forcément un incident. Il faut comparer durée, volume, plan SQL et historique.',
    '    AWR[AWR] --> DBTIME[DB Time]\n    ASH[ASH] --> SESS[Sessions]\n    CELLCLI[CellCLI] --> CELLMET[Métriques cellule]\n    ADR[ADR logs] --> ERR[Erreurs]\n    DBTIME --> DIAG[Diagnostic croisé]\n    CELLMET --> DIAG',
    'Aucun outil ne suffit seul ; la force vient du croisement entre temporalité, portée et couche.'
)

# Custom non-monitoring blocks
blocks['22-backup-and-recovery.md'] = r'''
## Complément expert V5 — Backup, recovery et Exadata

### Explication technique spécifique

Sur Exadata, RMAN lit les datafiles via ASM et peut écrire vers RECO, une librairie média, un ZDLRA, un stockage NFS ou un réseau de backup. La performance dépend de la bande passante cellule, du parallélisme RMAN, du débit cible, du redo généré, de la capacité RECO et de la concurrence avec les workloads SQL. Le design expert sépare sauvegarde locale rapide, copie externe, rétention, validation et scénario de restauration. Une sauvegarde réussie mais impossible à restaurer dans le RTO attendu n’est pas un design HA/DR satisfaisant.[^v5-rman]

```mermaid
flowchart LR
    DATA[Diskgroup DATA] --> RMAN[Canaux RMAN]
    RECO[Diskgroup RECO] --> RMAN
    RMAN --> FRA[Fast Recovery Area]
    RMAN --> MEDIA[Media Manager ou ZDLRA]
    RMAN --> NET[Réseau backup]
    RMAN --> CATALOG[Recovery Catalog]
```

### Exemple concret réaliste

Une base de 40 To est sauvegardée chaque nuit. Le backup commence vite puis ralentit lorsque RECO approche d’un seuil élevé et que l’archivage s’accumule. Le problème n’est pas forcément la lecture depuis DATA ; il peut venir du débit de destination, d’un nombre de canaux mal dimensionné, d’une compression coûteuse CPU ou d’une saturation réseau backup.

### Comment raisonner

Analyse RMAN par flux : source ASM, canaux, CPU, réseau, cible et catalogue. Vérifie aussi l’objectif de restauration : restaurer sur la même machine, sur un site DR, vers une appliance de récupération ou vers un environnement de test. Le nombre de canaux doit être cohérent avec la cible ; trop de canaux peut dégrader la production.

### Commandes / vues utiles

```sql
select * from v$rman_backup_job_details order by start_time desc fetch first 10 rows only;
select name, space_limit/1024/1024 mb_limit, space_used/1024/1024 mb_used from v$recovery_file_dest;
select sequence#, applied, archived, completion_time from v$archived_log order by sequence# desc fetch first 20 rows only;
```

```bash
asmcmd lsdg
cellcli -e "list metriccurrent where name like 'CD_IO%' attributes name,metricValue,objectName"
```

### Comment interpréter

Un backup lent peut être source-bound ou target-bound. Si les cellules lisent vite mais la cible écrit lentement, le réseau ou média manager est suspect. Si les waits RMAN montrent lecture lente et que les cellules sont chargées, la concurrence I/O est à étudier. Si RECO est sous pression, le risque immédiat peut être l’archivage et la capacité de récupération.

### Exercice pratique

Un backup RMAN dépasse sa fenêtre de nuit depuis trois jours. Donne un diagnostic read-only et une conclusion argumentée.

### Corrigé détaillé

Il faut lire `v$rman_backup_job_details`, vérifier la FRA avec `v$recovery_file_dest`, contrôler les archivelogs, ASM `lsdg`, métriques cellule et réseau backup. Si la durée augmente avec le volume d’archivelogs, la cause peut être fonctionnelle. Si le débit chute sans hausse de volume, la cible ou le réseau est suspect. La conclusion doit citer la preuve temporelle et la couche limitante.

### Limites et pièges

Ne pas confondre sauvegarde et restaurabilité. Ne pas activer compression ou chiffrement sans mesurer CPU. Ne pas utiliser RECO comme espace illimité. Un test de restore reste la preuve ultime.

### À retenir

Le backup Exadata est un pipeline. Le diagnostic expert identifie le maillon lent et vérifie que le RTO/RPO reste atteignable.

[^v5-rman]: Oracle, *Oracle Database Backup and Recovery User's Guide*, https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/
'''

blocks['23-ha-dr-et-maa.md'] = r'''
## Complément expert V5 — HA/DR, RAC, ASM, Data Guard et MAA

### Explication technique spécifique

La haute disponibilité Exadata combine plusieurs couches : redondance matérielle, ASM failure groups, Oracle RAC, services applicatifs, Data Guard, backups RMAN, flashback et procédures MAA. RAC protège contre la perte d’une instance ou d’un database server, ASM protège contre la perte de disques ou cellules selon redondance, Data Guard protège contre la perte de site ou corruption logique propagée selon configuration. MAA assemble ces capacités en architectures de référence et en pratiques testables.[^v5-maa]

```mermaid
flowchart LR
    APP[Applications] --> SVC[Services RAC]
    SVC --> RAC[RAC primary]
    RAC --> ASM[ASM DATA/RECO]
    ASM --> CELL[Storage cells]
    RAC --> DG[Data Guard redo transport]
    DG --> STBY[Standby site]
    RAC --> RMAN[Backups RMAN]
```

### Exemple concret réaliste

La perte d’un database server provoque une reconnexion des services vers les instances restantes ; la perte d’un disque est absorbée par ASM ; la perte d’un site impose Data Guard ou restauration. Ces incidents n’ont pas le même RTO. Un support expert doit donc apprendre à associer chaque panne à la couche qui la couvre et au test qui prouve cette couverture.

### Comment raisonner

Commence par nommer le scénario : panne instance, panne serveur, panne cellule, corruption, perte site, erreur humaine. Associe ensuite la protection : RAC, ASM, Data Guard, Flashback, RMAN. Enfin, vérifie les preuves : état services, lag Data Guard, état diskgroups, backups valides, tests de switchover ou restore.

### Commandes / vues utiles

```sql
select inst_id, instance_name, status from gv$instance order by inst_id;
select name, open_mode, database_role, switchover_status from v$database;
select name, value, unit from v$dataguard_stats;
select process, status, thread#, sequence# from v$managed_standby;
```

```bash
srvctl status database -d <DB_UNIQUE_NAME>
asmcmd lsdg
```

### Comment interpréter

Une base RAC ouverte ne prouve pas que le DR est prêt. Il faut vérifier le transport redo, l’application sur standby, le lag, les services, les backups et les procédures. Un `SUCCESS` ponctuel ne remplace pas un test de bascule documenté.

### Exercice pratique

Classe les protections nécessaires pour trois incidents : perte d’un disque, perte d’un database server et perte complète du site primaire.

### Corrigé détaillé

La perte d’un disque relève d’ASM et de la redondance cellule. La perte d’un database server relève de RAC, Clusterware et services. La perte du site primaire relève de Data Guard, éventuellement Far Sync, backups et runbook DR. La réponse est correcte car elle ne mélange pas HA locale et DR inter-site.

### Limites et pièges

Ne pas promettre un RTO sans test. Ne pas croire que RAC remplace Data Guard. Ne pas supposer qu’un standby est utilisable sans vérifier lag, services, paramètres et capacité.

### À retenir

MAA n’est pas un slogan : c’est l’alignement mesurable entre scénario de panne, mécanisme de protection et preuve de reprise.

[^v5-maa]: Oracle, *Oracle Maximum Availability Architecture*, https://www.oracle.com/database/technologies/high-availability/maa.html
'''

blocks['25-patching.md'] = r'''
## Complément expert V5 — Patching Exadata sans perte de contrôle

### Explication technique spécifique

Le patching Exadata concerne plusieurs couches : database home, Grid Infrastructure, Exadata System Software des cellules, firmware, OS des database servers, switches et agents. Le risque principal n’est pas seulement l’échec d’un patch ; c’est l’incohérence temporaire entre couches ou l’absence de plan de retour. Un patch rolling peut maintenir le service, mais seulement si RAC, services, redondance ASM, capacité restante et procédures sont vérifiés.[^v5-patching]

```mermaid
flowchart TD
    PRE[Pré-checks] --> GI[Grid Infrastructure]
    PRE --> DB[Database Homes]
    PRE --> CELL[Storage Cells]
    CELL --> ONE[Une cellule à la fois]
    GI --> RAC[RAC rolling]
    ONE --> POST[Post-checks]
    RAC --> POST
    POST --> DOC[Validation et preuves]
```

### Exemple concret réaliste

Avant de patcher une cellule, on vérifie que les diskgroups peuvent tolérer l’indisponibilité temporaire de ses grid disks. Pendant l’intervention, ASM peut resynchroniser après retour. Si une autre cellule est déjà dégradée, continuer le patch peut transformer une maintenance en incident. La fenêtre de patching doit donc intégrer l’état réel, pas seulement le calendrier.

### Comment raisonner

Le raisonnement patching part des prérequis : backups, état RAC, état ASM, absence de panne matérielle, versions actuelles, compatibilité et plan de rollback. Ensuite on ordonne les couches selon la procédure Oracle. Enfin on valide : versions, alertes, services, instances, diskgroups et performance de base.

### Commandes / vues utiles

```bash
opatch lsinventory
crsctl stat res -t
srvctl status database -d <DB_UNIQUE_NAME>
asmcmd lsdg
cellcli -e "list cell attributes name,releaseVersion,status"
cellcli -e "list alerthistory attributes severity,alertMessage,beginTime"
```

### Comment interpréter

Une commande de version réussie n’est pas une validation complète. Il faut vérifier l’état fonctionnel des services, l’absence d’alertes critiques, la capacité ASM et les symptômes post-maintenance. Une différence de version peut être attendue pendant rolling patch, mais elle doit être temporaire et documentée.

### Exercice pratique

Pourquoi faut-il vérifier ASM avant de patcher une storage cell ?

### Corrigé détaillé

Parce que le patch rendra potentiellement indisponibles des grid disks de cette cellule. ASM doit disposer de redondance et de capacité suffisantes pour maintenir les fichiers accessibles. Si un autre failure group est déjà dégradé, le patch augmente le risque. La réponse correcte relie patch cellule, grid disks, failure groups et disponibilité des fichiers.

### Limites et pièges

Ne pas patcher pour “tester” en production. Ne pas ignorer les alertes hardware avant maintenance. Ne pas confondre rolling avec sans impact : les performances peuvent baisser pendant la fenêtre.

### À retenir

Le patching Exadata est une opération de cohérence multi-couches. Les preuves avant et après patch comptent autant que la commande de patch elle-même.

[^v5-patching]: Oracle, *Oracle Exadata Database Machine Maintenance Guide*, https://docs.oracle.com/en/engineered-systems/exadata-database-machine/dbmmn/
'''

blocks['26-automated-support-ecosystem.md'] = r'''
## Complément expert V5 — ASR, diagnostics et écosystème support automatisé

### Explication technique spécifique

L’écosystème support Exadata associe alertes locales, diagnostics, Enterprise Manager, Auto Service Request, collecte SRDC, bundles ExaWatcher et procédures My Oracle Support. ASR peut ouvrir automatiquement des demandes de service pour certains défauts matériels, mais il ne remplace pas l’analyse DBA. Le rôle du support expert est de fournir des preuves propres : horodatage, composant, sévérité, impact, commandes read-only, historique et comparaison avec la période saine.[^v5-asr]

```mermaid
flowchart LR
    COMPONENT[Composant Exadata] --> ALERT[Alerte locale]
    ALERT --> EM[Enterprise Manager]
    ALERT --> ASR[Auto Service Request]
    DBA[DBA] --> SRDC[Collecte SRDC]
    SRDC --> MOS[My Oracle Support]
    ASR --> MOS
```

### Exemple concret réaliste

Une flash card signale des erreurs prédictives. ASR peut créer un SR, mais le DBA doit joindre l’état de la cellule, les alertes, la période d’impact et la confirmation que les bases restent disponibles. Cette documentation accélère le remplacement et évite les échanges inutiles avec le support.

### Comment raisonner

Sépare automatisation et décision. L’automatisation détecte, collecte ou ouvre ; la décision opérationnelle priorise, planifie et communique. Il faut vérifier si l’alerte est matérielle, logicielle, réseau ou supervision, puis collecter les preuves adaptées.

### Commandes / vues utiles

```bash
cellcli -e "list alerthistory attributes severity,alertMessage,beginTime"
cellcli -e "list cell detail"
cellcli -e "list physicaldisk detail"
adrci exec="show alert -tail 100"
```

### Comment interpréter

Un SR automatique ne prouve pas l’impact applicatif ; il prouve une condition supportable par Oracle. Inversement, une dégradation de performance peut exiger un SR même sans ASR. La qualité de la chronologie et des preuves détermine la rapidité d’escalade.

### Exercice pratique

Une alerte ASR est ouverte pour un composant flash. Que joins-tu au dossier support ?

### Corrigé détaillé

Il faut joindre alerte, détail cellule, détail composant, période, impact observé, état ASM, métriques I/O et versions. Le corrigé est correct car il fournit au support la chaîne composant-impact-preuve au lieu d’un message vague.

### Limites et pièges

Ne pas attendre qu’ASR ouvre tout. Ne pas envoyer des captures sans horodatage. Ne pas modifier la configuration pour “voir si ça passe” avant collecte.

### À retenir

Le support automatisé accélère la réaction, mais l’expertise DBA transforme l’alerte en diagnostic exploitable.

[^v5-asr]: Oracle, *Auto Service Request for Oracle Engineered Systems*, https://www.oracle.com/support/premier/auto-service-request.html
'''

blocks['27-exadata-cloud-service-et-cloud-customer.md'] = r'''
## Complément expert V5 — Exadata Cloud Service et Cloud@Customer

### Explication technique spécifique

Exadata Cloud Service et Exadata Cloud@Customer apportent Exadata dans un modèle opéré avec des responsabilités partagées. Le client conserve l’administration des bases, schémas, performances SQL, sauvegardes logiques et choix applicatifs ; Oracle gère une partie de l’infrastructure, du cycle de vie et des opérations cloud selon le service. La différence essentielle est le lieu d’exécution et le modèle opérationnel : Exadata Cloud Service s’exécute dans OCI, tandis que Cloud@Customer place l’infrastructure dans le datacenter client avec un contrôle cloud Oracle.[^v5-exacc]

```mermaid
flowchart LR
    DBA[DBA client] --> DB[Base Oracle]
    DB --> VM[VM Cluster]
    VM --> EXA[Infrastructure Exadata]
    OCI[Plan de contrôle OCI] --> VM
    ORA[Oracle Operations] --> EXA
    APP[Applications client] --> DB
```

### Exemple concret réaliste

Une équipe migre une base critique vers Exadata Cloud@Customer pour conserver la proximité réseau avec les applications on-premises. Les DBA doivent adapter leurs procédures : certaines opérations passent par OCI, les accès OS peuvent être encadrés, les sauvegardes peuvent utiliser des services cloud et les fenêtres de maintenance sont planifiées avec le modèle de service.

### Comment raisonner

Avant migration, il faut classifier les responsabilités : qui patche quoi, qui sauvegarde quoi, qui surveille quoi, qui ouvre les SR, qui valide la sécurité réseau et qui teste le DR. Ensuite, il faut comparer contraintes on-premises, latence, conformité, coûts, intégration IAM et exploitation quotidienne.

### Commandes / vues utiles

```sql
select name, open_mode, database_role from v$database;
select inst_id, instance_name, host_name, status from gv$instance;
select name, value from v$parameter where name in ('db_unique_name','cluster_database');
```

```bash
# Read-only : commandes locales selon droits disponibles
srvctl status database -d <DB_UNIQUE_NAME>
asmcmd lsdg
```

### Comment interpréter

Dans le cloud Exadata, l’absence d’accès à certaines couches n’est pas forcément une limitation anormale ; c’est parfois une frontière de responsabilité. Le diagnostic doit donc distinguer preuve technique accessible au DBA, métrique OCI, ticket Oracle et runbook interne.

### Exercice pratique

Explique pourquoi une procédure Exadata on-premises ne peut pas être copiée telle quelle vers Exadata Cloud@Customer.

### Corrigé détaillé

Parce que le modèle de responsabilité, les outils, les accès, les fenêtres de maintenance et l’intégration OCI changent. Les principes Oracle Database restent proches, mais les actions infrastructure peuvent relever d’Oracle ou du plan de contrôle cloud. La réponse correcte cite les responsabilités, l’accès, la supervision, les backups et la maintenance.

### Limites et pièges

Ne pas supposer que tous les accès root ou cellule sont disponibles. Ne pas ignorer les contraintes réseau OCI, IAM et maintenance. Ne pas comparer uniquement les performances ; l’exploitation et la conformité comptent autant.

### À retenir

Exadata Cloud et Cloud@Customer conservent les principes Exadata, mais changent fortement le modèle opérationnel et les responsabilités.

[^v5-exacc]: Oracle, *Oracle Exadata Cloud@Customer Documentation*, https://docs.oracle.com/en/cloud/cloud-at-customer/exadata-cloud-at-customer/
'''

for fname, block in blocks.items():
    upsert_block(fname, block)

print(f'V5 wave2 enriched: {len(blocks)} modules')
