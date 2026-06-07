from pathlib import Path
import json, re
ROOT = Path('/home/ubuntu/oracle-exadata-infra-ha-dr-course-labs-v4')
priority = [
 '02-architecture.md','06-exadata-storage-server-configuration.md','07-asm-et-modele-de-stockage.md','08-iorm.md','10-smart-scan.md','13-bulk-data-loading.md',
 '14-platform-monitoring-introduction.md','15-monitoring-exadata-system-software.md','16-enterprise-manager-cloud-control.md','17-monitoring-storage-servers.md','18-monitoring-database-servers.md','19-monitoring-network.md','20-monitoring-other-components.md','21-other-monitoring-tools.md',
 '22-backup-and-recovery.md','23-ha-dr-et-maa.md','25-patching.md','26-automated-support-ecosystem.md','27-exadata-cloud-service-et-cloud-customer.md'
]
generic_phrases = [
 'Dans Exadata, une décision prise sur une couche se répercute souvent sur les autres',
 'Le fonctionnement réel peut être résumé en trois niveaux',
 'Une bonne lecture technique consiste à comprendre le chemin',
 'Les commandes doivent être adaptées au contexte',
 'La recommandation finale doit rester proportionnée',
 'fait partie d’un ensemble Exadata intégré',
 'fait partie d\'un ensemble Exadata intégré',
 'un même symptôme peut avoir plusieurs causes',
 'il faut relier la mesure au composant concerné',
 'La première étape consiste à identifier la couche concernée'
]
required_sections = ['Comment raisonner','Commandes / vues utiles','Comment interpréter','Exercice pratique','Corrigé','À retenir','Limites et pièges']
report=[]
for fname in priority:
    p=ROOT/'modules'/fname
    txt=p.read_text(encoding='utf-8') if p.exists() else ''
    report.append({
        'file':fname,
        'exists':p.exists(),
        'words':len(txt.split()),
        'generic_hits':{ph:txt.count(ph) for ph in generic_phrases if txt.count(ph)},
        'has_mermaid':'```mermaid' in txt,
        'required_sections_missing':[s for s in required_sections if s.lower() not in txt.lower()],
        'cellcli_count':txt.lower().count('cellcli'),
        'asmcmd_count':txt.lower().count('asmcmd'),
        'sql_count':txt.lower().count('select '),
    })
summary={
 'priority_modules':len(priority),
 'existing_priority_modules':sum(r['exists'] for r in report),
 'total_generic_hits_priority':sum(sum(r['generic_hits'].values()) for r in report),
 'modules_without_mermaid':[r['file'] for r in report if not r['has_mermaid']],
 'modules_missing_required_sections':{r['file']:r['required_sections_missing'] for r in report if r['required_sections_missing']},
 'min_words_priority':min(r['words'] for r in report),
 'avg_words_priority':round(sum(r['words'] for r in report)/len(report),1),
}
Path('/home/ubuntu/v5_audit_report.json').write_text(json.dumps({'summary':summary,'modules':report},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
