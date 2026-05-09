"""Legacy Discord delivery entrypoint.

The maintained daily workflow is ``run_daily.sh`` or the GitHub Actions digest
job, both of which use the pluggable digest pipeline and static site output.
"""

from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Legacy Discord digest route")
    parser.add_argument("--dry-run", action="store_true", help="accepted for old scripts")
    parser.add_argument("--hours", type=int, default=None, help="accepted for old scripts")
    parser.parse_args()
    raise SystemExit(
        "Legacy Discord delivery has been removed; use run_daily.sh or digest_pipeline_gemini.py."
    )


if __name__ == "__main__":
    main()
