"""Vercel serverless entrypoint."""

import os
import sys

# 1. Mark this as a Vercel environment so paths.py uses /tmp
os.environ.setdefault("VERCEL", "1")

# 2. Ensure the project root is on sys.path so 'app' and
#    'news_research_tool' imports resolve correctly.
#    Vercel runs this file from the api/ directory.
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 3. Pre-create the /tmp runtime directories that logger.py and
#    exporter.py create at module-import time via mkdir(exist_ok=True).
#    Doing it here avoids any race between module imports.
os.makedirs("/tmp/logs", exist_ok=True)
os.makedirs("/tmp/reports", exist_ok=True)

# 4. Now it is safe to import the Flask app
from app import app  # noqa: E402

