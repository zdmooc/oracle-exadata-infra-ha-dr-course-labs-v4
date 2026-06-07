#!/usr/bin/env bash
set -euo pipefail
OUT=${1:-cell-evidence-$(date +%Y%m%d-%H%M%S)}
mkdir -p "$OUT"
if ! command -v cellcli >/dev/null; then echo 'cellcli introuvable sur cet hôte'; exit 0; fi
for q in 'list cell detail' 'list celldisk detail' 'list griddisk detail' 'list alerthistory' 'list metriccurrent'; do
  safe=$(echo "$q"|tr ' ' '_')
  cellcli -e "$q" > "$OUT/$safe.txt" 2>&1 || true
done
