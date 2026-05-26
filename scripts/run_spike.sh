#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: $0 <testcase.json> <run_id>"
  exit 1
fi

TESTCASE="$1"
RUN_ID="$2"
OUT_DIR="outputs/${RUN_ID}"
mkdir -p "${OUT_DIR}"

echo "[run_spike] testcase=${TESTCASE}"
# TODO: connect real Spike command here.

echo '{"runner":"spike","status":"stub","testcase":"'"${TESTCASE}"'"}' > "${OUT_DIR}/runner.json"
