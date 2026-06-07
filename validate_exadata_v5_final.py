from pathlib import Path
import json, re, subprocess, statistics

ROOT = Path('/home/ubuntu/oracle-exadata-infra-ha-dr-course-labs-v4')
MODULES = ROOT / 'modules'
PRIORITY = [
'02-architecture.md','06-exadata-storage-server-configuration.md','07-asm-et-modele-de-stockage.md','08-iorm.md','10-smart-scan.md','13-bulk-data-loading.md','14-platform-monitoring-introduction.md','15-monitoring-exadata-system-software.md','16-enterprise-manager-cloud-control.md','17-monitoring-storage-servers.md','18-monitoring-database-servers.md','19-monitoring-network.md','20-monitoring-other-components.md','21-other-monitoring-tools.md','22-backup-and-recovery.md','23-ha-dr-et-maa.md','25-patching.md','26-automated-support-ecosystem.md','27-exadata-cloud-service-et-cloud-customer.md']
GENERIC = [
'Dans Exadata, une décision prise sur une couche se répercute souvent sur les autres',
'Le fonctionnement réel peut être résumé en trois niveaux',
'Une bonne lecture technique consiste à comprendre le chemin',
'Les commandes doivent être adaptées au contexte',
'La recommandation finale doit rester proportionnée',
'fait partie d’un ensemble Exadata intégré',
'un même symptôme peut avoir plusieurs causes',
'il faut relier la mesure au composant concerné',
'La première étape consiste à identifier la couche concernée']
REQUIRED = ['Complément expert V5','Explication technique spécifique','Exemple concret réaliste','Comment raisonner','Commandes / vues utiles','Comment interpréter','Exercice pratique','Corrigé détaillé','Limites et pièges','À retenir']
DANGEROUS = re.compile(r'(^|\s)(rm\s+-rf|mkfs|dd\s+[^\n]*of=|shutdown\b|reboot\b|drop\s+diskgroup|drop\s+database|alter\s+system\s+set|cellcli\s+[^\n]*(?:drop|alter|create))', re.I)

def word_count(text):
    return len(re.findall(r"\b[\wÀ-ÿ']+\b", text))

priority_report = {}
for name in PRIORITY:
    path = MODULES / name
    text = path.read_text(encoding='utf-8') if path.exists() else ''
    priority_report[name] = {
        'exists': path.exists(),
        'words': word_count(text),
        'generic_hits': sum(text.count(g) for g in GENERIC),
        'has_mermaid': '```mermaid' in text,
        'missing_required_sections': [s for s in REQUIRED if s not in text],
        'dangerous_hits': [m.group(0).strip() for m in DANGEROUS.finditer(text)][:5]
    }

all_text_files = [p for p in ROOT.rglob('*') if p.is_file() and p.suffix.lower() in {'.md','.sh','.sql','.py','.txt','.yml','.yaml'} and '.git' not in p.parts]
active_dangerous = []
for p in all_text_files:
    text = p.read_text(encoding='utf-8', errors='ignore')
    for i,line in enumerate(text.splitlines(),1):
        stripped = line.strip()
        if stripped.startswith('#') or stripped.startswith('--'):
            continue
        if DANGEROUS.search(line):
            active_dangerous.append({'file': str(p.relative_to(ROOT)), 'line': i, 'text': stripped[:180]})

empty_files = [str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p.stat().st_size == 0 and '.git' not in p.parts]
module_files = list(MODULES.glob('*.md'))
lab_files = list((ROOT/'labs').rglob('*.md')) if (ROOT/'labs').exists() else []
mermaid_count = 0
for p in all_text_files:
    mermaid_count += p.read_text(encoding='utf-8', errors='ignore').count('```mermaid')

try:
    status = subprocess.check_output(['git','status','--short'], cwd=ROOT, text=True)
except Exception as e:
    status = f'git status error: {e}'

words = [r['words'] for r in priority_report.values()]
summary = {
    'priority_modules_expected': len(PRIORITY),
    'priority_modules_existing': sum(1 for r in priority_report.values() if r['exists']),
    'generic_hits_priority_total': sum(r['generic_hits'] for r in priority_report.values()),
    'priority_modules_without_mermaid': [k for k,r in priority_report.items() if not r['has_mermaid']],
    'priority_modules_missing_required_sections': {k:r['missing_required_sections'] for k,r in priority_report.items() if r['missing_required_sections']},
    'priority_modules_with_dangerous_hits': {k:r['dangerous_hits'] for k,r in priority_report.items() if r['dangerous_hits']},
    'active_dangerous_commands_repo': active_dangerous[:50],
    'empty_files': empty_files,
    'module_count': len(module_files),
    'lab_count': len(lab_files),
    'mermaid_count': mermaid_count,
    'min_words_priority': min(words),
    'avg_words_priority': round(statistics.mean(words),1),
    'git_status_short': status.strip(),
}

report = ['# Rapport de validation V5', '', '## Synthèse', '', '| Contrôle | Résultat |', '|---|---|']
for key in ['priority_modules_expected','priority_modules_existing','generic_hits_priority_total','module_count','lab_count','mermaid_count','min_words_priority','avg_words_priority']:
    report.append(f'| {key} | {summary[key]} |')
report += ['', '## Points bloquants', '']
blocking = []
if summary['generic_hits_priority_total'] != 0: blocking.append('Formulations génériques résiduelles dans les modules prioritaires.')
if summary['priority_modules_without_mermaid']: blocking.append('Modules prioritaires sans diagramme Mermaid.')
if summary['priority_modules_missing_required_sections']: blocking.append('Sections obligatoires manquantes.')
if summary['active_dangerous_commands_repo']: blocking.append('Commandes actives potentiellement risquées.')
if summary['empty_files']: blocking.append('Fichiers vides.')
report.append('Aucun point bloquant détecté.' if not blocking else '\n'.join(f'- {b}' for b in blocking))
report += ['', '## Détail modules prioritaires', '', '| Module | Mots | Générique | Mermaid | Sections manquantes |', '|---|---:|---:|---|---|']
for name,r in priority_report.items():
    report.append(f"| {name} | {r['words']} | {r['generic_hits']} | {'oui' if r['has_mermaid'] else 'non'} | {', '.join(r['missing_required_sections']) if r['missing_required_sections'] else 'aucune'} |")
report += ['', '## Git status', '', '```text', summary['git_status_short'] or 'working tree clean', '```', '', '## JSON brut', '', '```json', json.dumps(summary, indent=2, ensure_ascii=False), '```', '']

(Path('/home/ubuntu/v5_validation_report.md')).write_text('\n'.join(report), encoding='utf-8')
(Path('/home/ubuntu/v5_validation_summary.json')).write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps(summary, indent=2, ensure_ascii=False))
