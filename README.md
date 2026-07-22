# SmartVintaAwesomeKit

Smart Python developer toolkit — batteries-included project generator, configuration management, database utilities, and API helpers for modern Python applications.

## Quick Start

```bash
# Install
pip install smartvintaawesomekit

# Create a new project
smartvintaawesomekit init my-project
cd my-project

# Run the generated app
uvicorn app.main:app --reload
```

## Features

- **Smart Configuration** — pydantic-settings with sensible defaults
- **Smart Database** — Async SQLAlchemy session management + CRUD helpers
- **Smart API** — Standardized response formats, pagination, error handling
- **Smart CLI** — Project generator that scaffolds FastAPI apps in seconds
- **Testing Helpers** (P1) — Fixtures and utilities for testing FastAPI apps
- **Deployment Templates** (P1) — Railway-ready Dockerfile and configuration

## Development

```bash
# Install in editable mode with dev dependencies
uv pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Lint
ruff check .

# Type check
mypy src/
```

## License

MIT
