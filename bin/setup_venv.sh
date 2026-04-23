#!/bin/bash
# Local development environment setup

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .[dev]
pre-commit install

echo "Environment ready. Venv activated."
