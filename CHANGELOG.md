# Changelog

All notable changes to this project will be documented in this file.

## v0.1.0 — 2026-07-22

Initial MVP release of smartvintaawesomekit — a Smart Python developer toolkit.

### Features
- **Configuration management** — Pydantic V2 settings with environment variable loading, field descriptions, and `__all__` exports
- **Async SQLAlchemy 2.0 database** — Async session factory with `get_session()` generator, CRUD base class with create/read/update/delete operations, and graceful handling of `db=None` for smoke tests
- **FastAPI API layer** — Health check endpoint, generic request/response models, three exception handlers (validation, not-found, generic), and a `create_app()` factory
- **Typer CLI application** — Server management (start with configurable host/port/reload), version display, and `isinstance` guard for direct callback invocation
- **Packaging** — PEP 621 compliant `pyproject.toml` with `smartvintaawesomekit` CLI entry point

### Tests
- 105 tests total (91 interface + 14 behavioral) across 4 test modules
- `test_config.py` — 39 tests covering field presence, types, defaults, env loading, and optional config
- `test_database.py` — 29 tests covering session lifecycle, CRUD operations, and error handling
- `test_api.py` — 29 tests covering health endpoint, exception handlers, response models, and app factory
- `test_cli.py` — 8 tests covering CLI commands, flags, and version output
- Ruff linting clean (0 errors, 0 warnings)
