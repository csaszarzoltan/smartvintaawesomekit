"""Main FastAPI application for test-project."""

from fastapi import FastAPI

app = FastAPI(title="test-project")


@app.get("/")
async def root() -> dict[str, str]:
    """Health check endpoint."""
    return {"message": "Hello from test-project"}
