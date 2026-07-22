"""Pytest configuration and shared fixtures for smartvintaawesomekit tests."""

from __future__ import annotations

from typing import Any

import pytest


@pytest.fixture
def sample_env_file(tmp_path: Any) -> str:  # noqa: ANN401
    """Create a temporary .env file for config tests."""
    env_path = tmp_path / ".env"
    env_path.write_text(
        "APP_NAME=test-app\n"
        "ENVIRONMENT=testing\n"
        "LOG_LEVEL=DEBUG\n"
        "DATABASE_URL=sqlite+aiosqlite:///./test.db\n"
    )
    return str(env_path)
