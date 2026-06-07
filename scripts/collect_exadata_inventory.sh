#!/usr/bin/env bash
set -euo pipefail
OUT_DIR="${1:-./reports/local-inventory-$(date +%Y%m%d-%H%M%S)}"
mkdir -p "$OUT_DIR"
{
  echo "# Inventaire Exadata non destructif"
  echo "Date: $(date -Is)"
  echo "Host: $(hostname)"
  echo
  echo "## OS"
  uname -a || true
  uptime || true
  echo
  echo "## Image"
  imageinfo 2>/dev/null || true
  imagehistory 2>/dev/null || true
  echo
  echo "## CellCLI"
  cellcli -e "list cell attributes name,status,releaseVersion" 2>/dev/null || true
  cellcli -e "list celldisk attributes name,status,size" 2>/dev/null || true
  cellcli -e "list griddisk attributes name,status,size" 2>/dev/null || true
  echo
  echo "## DBMCLI"
  dbmcli -e "list dbserver" 2>/dev/null || true
} | tee "$OUT_DIR/inventory.md"
echo "Rapport généré dans $OUT_DIR/inventory.md"
