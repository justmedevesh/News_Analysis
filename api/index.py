"""Vercel serverless entrypoint."""

import os
import sys
import traceback

# 1. Mark this as a Vercel environment so paths.py uses /tmp
os.environ.setdefault("VERCEL", "1")

# 2. Ensure the project root is on sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 3. Pre-create /tmp runtime directories
os.makedirs("/tmp/logs", exist_ok=True)
os.makedirs("/tmp/reports", exist_ok=True)

# 4. Try importing the Flask app — capture the error if it fails
try:
    from app import app
except Exception:
    _import_error = traceback.format_exc()

    # Create a minimal WSGI app that shows the real error
    from flask import Flask
    app = Flask(__name__)

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def show_error(path):
        return (
            f"<h2>Import failed</h2>"
            f"<pre>{_import_error}</pre>"
            f"<hr>"
            f"<p>Python {sys.version}</p>"
            f"<p>sys.path: {sys.path}</p>"
            f"<p>cwd: {os.getcwd()}</p>"
            f"<p>project_root contents: {os.listdir(project_root) if os.path.isdir(project_root) else 'NOT FOUND'}</p>"
        ), 500
