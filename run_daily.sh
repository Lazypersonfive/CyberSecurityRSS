#!/usr/bin/env bash
# Run the daily multi-board pipeline locally. Pass one or more board names to
# only process a subset, e.g. ./run_daily.sh ai  or  ./run_daily.sh security ai.
# With no args, runs all three boards.
#
# Backend selection (env var):
#   LLM_BACKEND=gemini   (default) — uses digest_pipeline_gemini.py, needs GEMINI_API_KEY
#   LLM_BACKEND=anthropic          — uses digest_pipeline.py, needs ANTHROPIC_API_KEY

set -euo pipefail

cd "$(dirname "$0")"

PYTHON="${PYTHON:-/Users/dedsec/anaconda3/envs/work3124/bin/python}"
LLM_BACKEND="${LLM_BACKEND:-gemini}"

case "$LLM_BACKEND" in
  gemini) DIGEST_SCRIPT=digest_pipeline_gemini.py ;;
  anthropic) DIGEST_SCRIPT=digest_pipeline.py ;;
  *) echo "unknown LLM_BACKEND=$LLM_BACKEND" >&2; exit 1 ;;
esac

echo "LLM backend: $LLM_BACKEND ($DIGEST_SCRIPT)"

BOARDS=("$@")
if [ ${#BOARDS[@]} -eq 0 ]; then
  BOARDS=(security ai finance)
fi

for board in "${BOARDS[@]}"; do
  echo ""
  echo "=========================================="
  echo "  Board: $board"
  echo "=========================================="
  "$PYTHON" fetch_and_save.py --board "$board"
  "$PYTHON" "$DIGEST_SCRIPT" --board "$board"
done

echo ""
echo "=========================================="
echo "  Build site"
echo "=========================================="
"$PYTHON" site_builder.py

echo ""
echo "Done. Open docs/index.html to preview."
