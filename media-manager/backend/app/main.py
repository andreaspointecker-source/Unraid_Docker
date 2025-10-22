"""Main FastAPI application."""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import init_db

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager.

    Handles startup and shutdown events.
    """
    # Startup
    logger.info(f"Starting {settings.app_name}...")
    logger.info(f"Environment: {settings.app_env}")
    logger.info(f"Debug mode: {settings.debug}")

    # Ensure directories exist
    try:
        settings.ensure_directories()
        logger.info("Directories verified")
    except Exception as e:
        logger.error(f"Failed to create directories: {e}")

    # Initialize database
    try:
        init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

    logger.info(f"{settings.app_name} started successfully")

    yield

    # Shutdown
    logger.info(f"Shutting down {settings.app_name}...")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Automated download, extraction, encoding, and media management for Unraid",
    version="1.0.0-alpha",
    lifespan=lifespan,
    docs_url="/api/docs" if settings.debug else None,
    redoc_url="/api/redoc" if settings.debug else None,
)

# CORS middleware
if settings.enable_cors:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.debug else "An error occurred",
        },
    )


# Health check endpoint
@app.get("/api/health", tags=["System"])
async def health_check():
    """
    Health check endpoint for monitoring.

    Returns:
        dict: Health status
    """
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": "1.0.0-alpha",
        "environment": settings.app_env,
    }


# Root endpoint
@app.get("/api", tags=["System"])
async def root():
    """
    Root API endpoint.

    Returns:
        dict: API information
    """
    return {
        "app": settings.app_name,
        "version": "1.0.0-alpha",
        "docs": "/api/docs" if settings.debug else None,
    }


# Mount static files (frontend) - only in production
# In development, frontend is served by Vite dev server
try:
    from pathlib import Path

    frontend_dist = Path(__file__).parent.parent.parent / "frontend" / "dist"
    if frontend_dist.exists() and settings.app_env == "production":
        app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="static")
        logger.info("Frontend static files mounted")
except Exception as e:
    logger.warning(f"Could not mount frontend static files: {e}")


# Import and include routers
from app.api import downloads

app.include_router(downloads.router, prefix="/api/downloads", tags=["Downloads"])

# These will be added as we implement each module
# from app.api import encoding, tmdb, settings, accounts, passwords, workers
# app.include_router(encoding.router, prefix="/api/encoding", tags=["Encoding"])
# app.include_router(tmdb.router, prefix="/api/tmdb", tags=["TMDB"])
# app.include_router(settings.router, prefix="/api/settings", tags=["Settings"])
# app.include_router(accounts.router, prefix="/api/accounts", tags=["Accounts"])
# app.include_router(passwords.router, prefix="/api/passwords", tags=["Passwords"])
# app.include_router(workers.router, prefix="/api/workers", tags=["Workers"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
