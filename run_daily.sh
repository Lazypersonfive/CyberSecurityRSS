#!/usr/bin/env bash
# Run the daily multi-board pipeline locally. Pass one or more board names to
# only process a subset, e.g. ./run_daily.sh ai_security  or  ./run_daily.sh security ai.
# With no args, runs all configured boards.
#
# Backend selection (env var):
#   LLM_BACKEND=gemini   (default) — needs GEMINI_API_KEY
#   LLM_BACKEND=deepseek           — needs DEEPSEEK_API_KEY

set -euo pipefail

cd "$(dirname "$0")"

PYTHON="${PYTHON:-/Users/dedsec/anaconda3/envs/work3124/bin/python}"
LLM_BACKEND="${LLM_BACKEND:-gemini}"

case "$LLM_BACKEND" in
  gemini|deepseek) ;;
  *) echo "unknown LLM_BACKEND=$LLM_BACKEND" >&2; exit 1 ;;
esac

echo "LLM backend: $LLM_BACKEND (digest_pipeline_gemini.py)"

BOARDS=("$@")
if [ ${#BOARDS[@]} -eq 0 ]; then
  BOARDS=(security ai_security ai finance)
fi

for board in "${BOARDS[@]}"; do
  echo ""
  echo "=========================================="
  echo "  Board: $board"
  echo "=========================================="
  "$PYTHON" fetch_and_save.py --board "$board"
  "$PYTHON" digest_pipeline_gemini.py --board "$board"
done

echo ""
echo "=========================================="
echo "  Build site"
echo "=========================================="
"$PYTHON" site_builder.py

echo ""
echo "=========================================="
echo "  Build source audit"
echo "=========================================="
"$PYTHON" source_audit.py

echo ""
echo "Done. Open docs/index.html to preview."
