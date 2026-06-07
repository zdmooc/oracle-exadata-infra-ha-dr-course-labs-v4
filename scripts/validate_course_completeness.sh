#!/usr/bin/env bash
set -euo pipefail
missing=0
for i in $(seq -w 0 27); do
  if ! ls modules/${i}-*.md >/dev/null 2>&1; then echo "Module manquant: $i"; missing=1; fi
done
for f in docs/04-mapping-syllabus-oracle-university.md docs/05-glossaire-exadata.md docs/07-criteres-completude.md docs/99-rapport-completude-final.md; do
  [ -f "$f" ] || { echo "Document manquant: $f"; missing=1; }
done
exit $missing
