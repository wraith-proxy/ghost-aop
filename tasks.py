import subprocess
import sys
from pathlib import Path

import typer


def setup() -> None:
    """Set up the development environment."""
    typer.echo("--- Ghost Stack: Template Orchestrator ---")

    # 1. Environment Prep
    env_file = Path(".env")
    if not env_file.exists():
        typer.echo(
            "Creating default .env... (Welcome to the defaults you didn't ask for)"
        )
        env_file.write_text("APP_NAME=ghost-template\nDEBUG=true\n")

    try:
        typer.echo("📦 Syncing dependencies with uv... (Go get a coffee, or a life)")
        subprocess.run(["uv", "sync", "--all-extras"], check=True)

        git_dir = Path(".git")
        if git_dir.exists() and git_dir.is_dir():
            typer.echo(
                "🪝 Ensuring pre-commit hooks are installed..."
                " because you'll forget otherwise."
            )
            subprocess.run(["uv", "run", "pre-commit", "install"], check=True)

        typer.echo("✅ Setup complete! You can now run tasks using 'uv run poe <task>'")
    except subprocess.CalledProcessError as e:
        typer.echo(f"❌ Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    setup()
