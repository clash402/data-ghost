"""Main FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.core.config import settings
from src.core.logging import get_logger, setup_logging
from src.routers import upload_router, query_router, health_router

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting Data Ghost Backend...")
    logger.info(f"Environment: {'Development' if settings.debug else 'Production'}")
    logger.info(f"ChromaDB Path: {settings.chroma_db_path}")
    logger.info(f"Upload Directory: {settings.upload_dir}")

    yield

    # Shutdown
    logger.info("Shutting down Data Ghost Backend...")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    # Initialize logging
    setup_logging()

    # Create FastAPI app
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Backend API for Data Ghost - CSV data analysis with AI",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        lifespan=lifespan,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(health_router)
    app.include_router(upload_router)
    app.include_router(query_router)

    # Root endpoint
    @app.get("/")
    async def root():
        return {
            "message": "Data Ghost Backend API",
            "version": settings.app_version,
            "docs": (
                "/docs" if settings.debug else "Documentation disabled in production"
            ),
        }

    return app


# Create the application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8080,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
