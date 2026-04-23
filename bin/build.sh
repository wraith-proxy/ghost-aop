#!/bin/bash
set -e

echo "--- Ghost Stack: Template Orchestrator ---"

# 1. Environment Prep
if [ ! -f .env ]; then
    echo "Creating default .env..."
    cat <<EOF > .env
APP_NAME=ghost-template
DEBUG=true
EOF
fi

# 2. Check for UV (The Sovereign Package Manager)
if ! command -v uv &> /dev/null; then
    echo "UV not found. Installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

# 3. Sync Workspace
echo "Syncing Python environment..."
uv sync

# 4. Build Container
echo "Building Ghost container..."
docker compose build

echo "--- Ghost is Ready. Run with 'docker compose up' ---"
