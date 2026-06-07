# Critères de complétude V3

| Critère | Attendu | Validation |
|---|---:|---|
| Modules | 28 modules 00 à 27 | `scripts/completeness-check.sh` |
| Labs | 19 labs ciblés | `scripts/completeness-check.sh` |
| Templates | 25+ modèles opérationnels | Comptage fichiers `templates/` |
| Diagrammes Mermaid | 12+ diagrammes `.mmd` | Comptage et inspection Mermaid |
| Scripts read-only | 8+ scripts | Inspection scripts et détecteur risques |
| Contenu spécifique | Pas de mini-lab identique partout | Audit `docs/98-audit-contenu-generique.md` |
| Sécurité | Commandes risquées absentes ou signalées | `scripts/dangerous-command-detector.sh` |
