"""Vercel serverless entrypoint with raw WSGI diagnostic fallback."""

import os
import sys
import traceback

# 1. Environment setup
os.environ.setdefault("VERCEL", "1")

# 2. Add project root to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 3. Pre-create /tmp directories
os.makedirs("/tmp/logs", exist_ok=True)
os.makedirs("/tmp/reports", exist_ok=True)

# 4. Try importing the real app
_boot_error = None
try:
    from app import app
except Exception:
    _boot_error = traceback.format_exc()
    app = None


# 5. If import failed, create a raw WSGI fallback (zero dependencies)
if app is None:
    # Collect diagnostic info
    _diag_lines = [
        f"Python: {sys.version}",
        f"CWD: {os.getcwd()}",
        f"project_root: {project_root}",
        f"project_root exists: {os.path.isdir(project_root)}",
        "",
        "--- project_root listing ---",
    ]
    try:
        _diag_lines += sorted(os.listdir(project_root))
    except Exception as e:
        _diag_lines.append(f"listdir error: {e}")

    _diag_lines += [
        "",
        "--- sys.path ---",
        *sys.path,
        "",
        "--- pip packages ---",
    ]
    try:
        import subprocess
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--format=columns"],
            capture_output=True, text=True, timeout=10,
        )
        _diag_lines.append(result.stdout or "(empty)")
        if result.stderr:
            _diag_lines.append(result.stderr)
    except Exception as e:
        _diag_lines.append(f"pip list error: {e}")

    _diag_lines += ["", "--- IMPORT ERROR ---", _boot_error or "(none)"]

    _body = "\n".join(_diag_lines)

    def app(environ, start_response):
        """Minimal WSGI app that shows diagnostics."""
        status = "500 Internal Server Error"
        headers = [("Content-Type", "text/plain; charset=utf-8")]
        start_response(status, headers)
        return [_body.encode("utf-8")]
