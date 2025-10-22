"""Database configuration and session management."""

import logging
from typing import AsyncGenerator

from sqlalchemy import create_engine, event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.config import settings

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


# Determine if using SQLite
is_sqlite = settings.database_url.startswith("sqlite")

# Create engine based on database type
if is_sqlite:
    # SQLite: Use synchronous engine with proper configuration
    DATABASE_URL = settings.database_url.replace("sqlite:///", "sqlite+pysqlite:///")

    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=settings.debug,
    )

    # Enable WAL mode for better concurrency
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA cache_size=-64000")  # 64MB cache
        cursor.execute("PRAGMA temp_store=MEMORY")
        cursor.close()

    # Session factory
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

else:
    # PostgreSQL or other databases: Use async engine
    engine = create_async_engine(
        settings.database_url,
        echo=settings.debug,
        pool_pre_ping=True,
    )

    # Async session factory
    SessionLocal = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


def init_db() -> None:
    """
    Initialize database and create all tables.

    This should be called on application startup.
    """
    try:
        logger.info("Initializing database...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


def get_db() -> Session:
    """
    Get database session dependency for FastAPI.

    Yields:
        Session: Database session

    Example:
        ```python
        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
        ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Get async database session dependency for FastAPI.

    Yields:
        AsyncSession: Async database session

    Example:
        ```python
        @app.get("/items")
        async def read_items(db: AsyncSession = Depends(get_async_db)):
            result = await db.execute(select(Item))
            return result.scalars().all()
        ```
    """
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def drop_db() -> None:
    """
    Drop all database tables.

    WARNING: This will delete all data!
    Use only for testing or development.
    """
    logger.warning("Dropping all database tables...")
    Base.metadata.drop_all(bind=engine)
    logger.warning("All tables dropped")


def reset_db() -> None:
    """
    Reset database by dropping and recreating all tables.

    WARNING: This will delete all data!
    Use only for testing or development.
    """
    drop_db()
    init_db()
