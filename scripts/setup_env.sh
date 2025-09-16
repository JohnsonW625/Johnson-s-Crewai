#!/usr/bin/env bash
# Creates a Python virtual environment and installs dependencies from requirements.txt
# Usage: ./scripts/setup_env.sh
set -euo pipefail
PYTHON=${PYTHON:-python3}
VENV_DIR=${VENV_DIR:-.venv}

echo "Creating virtual environment in $VENV_DIR using $PYTHON..."
$PYTHON -m venv "$VENV_DIR"

echo "Installing pip and wheel upgrades..."
"$VENV_DIR/bin/pip" install --upgrade pip wheel

echo "Installing requirements.txt..."
"$VENV_DIR/bin/pip" install -r requirements.txt

cat <<'MSG'

Done.
To activate the virtual environment (zsh):

  source .venv/bin/activate

Then run the program:

  python main.py

MSG
