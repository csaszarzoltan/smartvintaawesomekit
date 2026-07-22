"""SmartVintaAwesomeKit — ASGI application entry point for Railway deployment.

Provides a minimal FastAPI demo app that showcases the toolkit's API utilities,
including the health endpoint, standardized response models, and exception handlers.
"""
from __future__ import annotations

from fastapi import FastAPI

from smartvintaawesomekit.api import register_exception_handlers

app = FastAPI(
    title="SmartVintaAwesomeKit",
    version="0.1.0",
    description="Smart Python developer toolkit — API demo",
)


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "version": "0.1.0"}


@app.get("/")
async def root() -> dict[str, str | list[str]]:
    """Root endpoint with available routes."""
    return {
        "name": "SmartVintaAwesomeKit",
        "version": "0.1.0",
        "endpoints": ["/health", "/docs", "/openapi.json"],
    }


register_exception_handlers(app)
