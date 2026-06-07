"""Vercel serverless entrypoint."""

import os
import sys

# Ensure the project root directory is in the Python path
# This prevents ModuleNotFoundError on Vercel when importing root packages/modules
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app import app
