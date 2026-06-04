"""Central filesystem paths used by the application."""

import os
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PACKAGE_DIR.parent
IS_VERCEL = os.getenv("VERCEL") == "1"
RUNTIME_DIR = Path("/tmp") if IS_VERCEL else PROJECT_ROOT
LOGS_DIR = RUNTIME_DIR / "logs"
REPORTS_DIR = RUNTIME_DIR / "reports"
