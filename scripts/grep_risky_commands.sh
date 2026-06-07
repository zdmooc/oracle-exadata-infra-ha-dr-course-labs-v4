#!/usr/bin/env bash
set -euo pipefail
ROOT=${1:-.}
grep -RInE '(drop|delete|modify|alter|restart|shutdown|startup|patch|apply|rebalance|rm -rf)' "$ROOT" --include='*.md' --include='*.sh' --include='*.sql' || true
