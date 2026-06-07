#!/usr/bin/env bash
set -euo pipefail
find . -name '*.md' -not -path './.git/*' -print | sort
printf '
Validation basique terminée : fichiers Markdown listés.
'
