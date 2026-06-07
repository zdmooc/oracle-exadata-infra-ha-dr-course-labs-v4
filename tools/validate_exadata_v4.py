from pathlib import Path
import re, json
ROOT=Path('/home/ubuntu/oracle-exadata-infra-ha-dr-course-labs-work_v2-v3')
mods=sorted((ROOT/'modules').glob('*.md'))
phrases=['l’apprenant doit savoir reconnaître','produire une preuve observable','collecter des preuves','interpréter prudemment','relier à la couche concernée','rédiger une conclusion','aucun seuil universel n’est inventé']
required=[f'## {i}.' for i in range(1,14)]
report=[]
ok=True
for p in mods:
    txt=p.read_text(encoding='utf-8')
    missing=[h for h in required if h not in txt]
    counts={ph:txt.count(ph) for ph in phrases if txt.count(ph)}
    has_concepts='| Concept | Définition claire | Exemple concret |' in txt
    has_ex='## 11. Exercice pratique' in txt and '## 12. Corrigé de l’exercice' in txt
    words=len(txt.split())
    item={'file':str(p.relative_to(ROOT)),'words':words,'missing_sections':missing,'generic_counts':counts,'has_concept_table':has_concepts,'has_exercise_and_correction':has_ex}
    if missing or counts or not has_concepts or not has_ex or words<1200:
        ok=False
    report.append(item)
# active dangerous commands in markdown/code excluding detector itself
danger_patterns=[r'\brm\s+-rf\b',r'\bmkfs\b',r'\bdd\s+if=',r'\bdrop\s+database\b',r'\bshutdown\s+abort\b']
danger=[]
for p in ROOT.rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.md','.sh','.sql','.py'} and '.git' not in p.parts:
        txt=p.read_text(encoding='utf-8',errors='ignore').lower()
        if p.name in {'dangerous-command-detector.sh'}:
            continue
        for pat in danger_patterns:
            if re.search(pat,txt):
                danger.append((str(p.relative_to(ROOT)),pat))
summary={
    'module_count':len(mods),
    'all_modules_have_required_structure':all(not r['missing_sections'] for r in report),
    'generic_phrase_occurrences_in_modules':sum(sum(r['generic_counts'].values()) for r in report),
    'all_modules_have_concept_table':all(r['has_concept_table'] for r in report),
    'all_modules_have_exercise_and_correction':all(r['has_exercise_and_correction'] for r in report),
    'min_words_per_module':min(r['words'] for r in report),
    'avg_words_per_module':round(sum(r['words'] for r in report)/len(report),1),
    'dangerous_active_matches':danger,
    'ok':ok and len(mods)==28 and not danger
}
Path('/home/ubuntu/v4_validation_report.json').write_text(json.dumps({'summary':summary,'modules':report},ensure_ascii=False,indent=2),encoding='utf-8')
Path('/home/ubuntu/v4_validation_report.md').write_text('# Rapport de validation V4\n\n'+'\n'.join([
    f"| Modules | {summary['module_count']} |",
    f"| Structure 1-13 complète | {summary['all_modules_have_required_structure']} |",
    f"| Occurrences génériques ciblées dans modules | {summary['generic_phrase_occurrences_in_modules']} |",
    f"| Tables de concepts présentes | {summary['all_modules_have_concept_table']} |",
    f"| Exercices et corrigés présents | {summary['all_modules_have_exercise_and_correction']} |",
    f"| Minimum mots/module | {summary['min_words_per_module']} |",
    f"| Moyenne mots/module | {summary['avg_words_per_module']} |",
    f"| Commandes dangereuses actives détectées | {len(summary['dangerous_active_matches'])} |",
    f"| Validation globale | {summary['ok']} |",
])+'\n',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
