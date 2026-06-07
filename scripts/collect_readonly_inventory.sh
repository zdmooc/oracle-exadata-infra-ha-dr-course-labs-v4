#!/usr/bin/env bash
set -euo pipefail
OUT=${1:-evidence-$(date +%Y%m%d-%H%M%S)}
mkdir -p "$OUT"
run(){ echo "## $*" | tee -a "$OUT/commands.log"; "$@" > "$OUT/$(echo "$*"|tr ' /' '__').txt" 2>&1 || true; }
run hostname -f
run date
run uname -a
run df -h
run ip -br addr
command -v crsctl >/dev/null && run crsctl stat res -t
command -v srvctl >/dev/null && run srvctl status database -v
command -v asmcmd >/dev/null && run asmcmd lsdg
command -v cellcli >/dev/null && run cellcli -e 'list cell detail'
