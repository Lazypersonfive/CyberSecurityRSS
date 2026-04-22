#!/usr/bin/env bash
# Run the daily multi-board pipeline locally. Pass one or more board names to
# only process a subset, e.g. ./run_daily.sh ai  or  ./run_daily.sh security ai.
# With no args, runs all three boards.

set -euo pipefail

cd "$(dirname "$0")"

PYTHON="${PYTHON:-/Users/dedsec/anaconda3/envs/work3124/bin/python}"

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
  "$PYTHON" digest_pipeline.py --board "$board"
done

echo ""
echo "=========================================="
echo "  Build site"
echo "=========================================="
"$PYTHON" site_builder.py

echo ""
echo "Done. Open docs/index.html to preview."
