# ghost-aop

Aspect-Oriented Programming in Python — a working example of cross-cutting concerns
(logging, retry, and lineage tracking) applied transparently to a data pipeline using
[`aspectlib`](https://python-aspectlib.readthedocs.io/).

## What it does

The project wraps a classic ETL pipeline in three aspects woven at import time:

| Aspect | Behaviour |
|---|---|
| `log_execution` | Logs entry, exit, and elapsed time for every stage |
| `retry` | Retries any stage that raises `TransientError` up to 3 times |
| `audit_trail` | Appends an input/output lineage record to `LineageStore` after each stage |

The stages themselves (`ExtractStage`, `TransformStage`, `LoadStage`) contain only
business logic. They know nothing about logging, retries, or lineage — that concern
lives entirely in `aspects.py` and is woven in by `pipeline/__init__.py`.

## Project layout

```
src/
├── main.py              # Entrypoint — run with `ghost-run` or `uv run poe run`
└── pipeline/
    ├── __init__.py      # Weaves aspects onto all stages at import time
    ├── aspects.py       # log_execution, retry, audit_trail, LineageStore
    ├── models.py        # DataBatch, ProcessedBatch dataclasses
    └── stages.py        # ExtractStage, TransformStage, LoadStage
tests/
├── conftest.py          # Shared fixtures (lineage store reset between tests)
├── test_aspects.py      # Aspect behaviours in isolation with local test classes
├── test_models.py       # DataBatch / ProcessedBatch field and default validation
└── test_stages.py       # Stage execute() logic and parametrised edge cases
```

## Getting started

### Prerequisites

- Python >= 3.12
- [`uv`](https://github.com/astral-sh/uv)
  - **macOS/Linux**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - **Windows**: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

### Installation

```bash
git clone <repository-url>
cd ghost-aop
uv run poe setup        # syncs deps + installs pre-commit hooks
```

### Run the pipeline demo

```bash
ghost-run               # installed entrypoint
# or
uv run python -m src.main
```

Output shows log lines from all three aspects followed by the lineage trail:

```
=== PIPELINE RUN ===

12:00:00 [INFO] [ExtractStage] Starting
12:00:00 [INFO] [ExtractStage] Done in 0.0001s
12:00:00 [INFO]   [LINEAGE] {'stage': 'ExtractStage', ...}
...

=== LINEAGE TRAIL ===

  {'stage': 'ExtractStage', 'input_id': '...', 'output_id': '...', 'timestamp': '...'}
  {'stage': 'TransformStage', ...}
  {'stage': 'LoadStage', ...}
```

## Development

```bash
uv run poe test         # pytest (interactive)
uv run poe test-ci      # pytest with coverage enforcement (≥80%)
uv run poe lint         # ruff check
uv run poe format       # ruff format
```

### Committing

All commits go through `commitizen` with the Ghost Stack convention:

```
👻 <type>/<ticket>: <message>
```

```bash
uv run cz commit
```

## How AOP works here

`aspectlib` uses the generator-coroutine protocol. An `@aspectlib.Aspect` function
yields `Proceed` to call the original method, receives the return value, and can
yield `Return(value)` to replace it. This lets each aspect compose cleanly:

```python
@aspectlib.Aspect
def retry(*args, **kwargs):
    for attempt in range(3):
        try:
            result = yield aspectlib.Proceed
            yield aspectlib.Return(result)
            return
        except TransientError:
            if attempt == 2:
                raise
```

`pipeline/__init__.py` weaves all three aspects onto all three stages once, before any
code outside the package can instantiate them. No decorators on the stages, no
inheritance, no mixins.
