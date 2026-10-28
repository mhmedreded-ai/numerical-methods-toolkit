#!/usr/bin/env bash
# ==============================================================
# Math 3 - Numerical Analysis Suite (Linux & macOS Launcher)
# ==============================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Detect Python virtual environment or system Python
if [ -f ".venv/bin/python" ]; then
    PY_BIN=".venv/bin/python"
elif [ -f "venv/bin/python" ]; then
    PY_BIN="venv/bin/python"
elif command -v python3 &>/dev/null; then
    PY_BIN="python3"
elif command -v python &>/dev/null; then
    PY_BIN="python"
else
    echo "[ERROR] Python 3 was not found in PATH." >&2
    echo "Please install Python 3.10+ (e.g. brew install python3 or sudo apt install python3 python3-tk)." >&2
    exit 1
fi

if [ "$1" = "--mobile" ]; then
    echo "Starting Math 3 Mobile App (Kivy) using $PY_BIN..."
    exec "$PY_BIN" mobile_app.py "${@:2}"
else
    echo "Starting Math 3 Desktop GUI using $PY_BIN..."
    exec "$PY_BIN" app.py "$@"
fi
