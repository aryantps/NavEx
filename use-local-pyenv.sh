#!/bin/bash

# Script to fix pyenv + poetry mismatch for local terminal session
# Usage: source use-local-pyenv.sh

unset PYENV_VERSION  # Remove any forced override

PROJECT_PY_VERSION="3.13.5"

# Check if Python version is installed
if ! pyenv versions --bare | grep -q "^${PROJECT_PY_VERSION}$"; then
    echo "Python $PROJECT_PY_VERSION not found. Installing..."
    pyenv install "$PROJECT_PY_VERSION"
fi

echo "Activating Python $PROJECT_PY_VERSION locally..."
pyenv local "$PROJECT_PY_VERSION"

PYTHON_BIN="$(pyenv which python)"

echo "Using Python: $PYTHON_BIN"
"$PYTHON_BIN" --version

# Set poetry to use the correct Python
echo "Setting Poetry environment..."
poetry env use "$PYTHON_BIN"

# echo "Installing dependencies..."
# poetry install
