"""Central filesystem paths used by the application."""

import os
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PACKAGE_DIR.parent

# Detect Vercel or other serverless/read-only hosting environments
IS_VERCEL = os.getenv("VERCEL") == "1" or os.getenv("NOW_REGION") is not None

def get_runtime_dir() -> Path:
    if IS_VERCEL:
        return Path("/tmp")
    
    # Fallback check: test if the project root is writable
    try:
        test_file = PROJECT_ROOT / ".write_test"
        test_file.write_text("test", encoding="utf-8")
        test_file.unlink()
        return PROJECT_ROOT
    except Exception:
        return Path("/tmp")

RUNTIME_DIR = get_runtime_dir()
LOGS_DIR = RUNTIME_DIR / "logs"
REPORTS_DIR = RUNTIME_DIR / "reports"
