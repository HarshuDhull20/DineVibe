import ssl
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from sqlalchemy.orm import declarative_base
from app.config.settings import settings

# =====================================================
# SSL CONFIGURATION (AWS RDS REQUIREMENT)
# =====================================================
# AWS RDS uses encrypted connections.
# We create an SSL context to securely connect to PostgreSQL.

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# =====================================================
# DATABASE ENGINE
# =====================================================
# Using async SQLAlchemy + asyncpg for high concurrency
# This is how real production FastAPI apps work

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,                       # Turn ON only for debugging
    pool_pre_ping=True,               # Ensures stale connections are recycled
    pool_size=10,                     # Base number of connections
    max_overflow=20,                  # Extra connections during peak load
    connect_args={"ssl": ssl_context} # Required for AWS RDS SSL
)

# =====================================================
# SESSION FACTORY
# =====================================================
# Every API request gets its own DB session
# Sessions are short-lived and safely closed

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# =====================================================
# BASE MODEL
# =====================================================
# All models (User, Session, AuditLog, etc.)
# inherit from this Base

Base = declarative_base()

# =====================================================
# DATABASE DEPENDENCY
# =====================================================
# This is injected into FastAPI routes using Depends()

async def get_db():
    """
    Yields a database session per request.
    Ensures clean open/close lifecycle.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# =====================================================
# DATABASE INITIALIZER
# =====================================================
# Used during startup & seed.py

async def init_db():
    """
    Creates all database tables based on models.
    Used only during initial setup or migrations.
    """
    async with engine.begin() as conn:
        import app.models  # Import here to avoid circular imports
        await conn.run_sync(Base.metadata.create_all)
