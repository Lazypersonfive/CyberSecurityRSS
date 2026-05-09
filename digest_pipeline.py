"""Legacy compatibility entrypoint for the pluggable digest pipeline.

Use digest_pipeline_gemini.py directly for new automation. This file remains so
older scripts that call ``python digest_pipeline.py --board ...`` still execute
the current backend-selected pipeline.
"""

from __future__ import annotations

from digest_pipeline_gemini import main, run

__all__ = ["main", "run"]


if __name__ == "__main__":
    main()
