# Aspect Oriented Programming in Python

## Getting Started

### Prerequisites
- Python >= 3.12
- [uv](https://github.com/astral-sh/uv) for dependency management. Install it via:
  - **macOS/Linux**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - **Windows**: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd <repository-directory>

# Run the setup task
uv run poe setup
```

### Running Tests

```bash
# Run the test suite
uv run poe test

# Run tests with coverage enforcement (CI style)
uv run poe test-ci
```