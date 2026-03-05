import ssl
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from sqlalchemy.orm import declarative_base
from app.config.settings import settings

# =====================================================
# SSL CONFIGURATION
# =====================================================
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# =====================================================
# DATABASE ENGINE
# =====================================================
# ✅ Vercel serverless: NO connection pooling
# Each function invocation gets its own connection

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    # ✅ Serverless-compatible settings
    pool_size=1,
    max_overflow=0,
    pool_recycle=300,
    connect_args={"ssl": ssl_context}
)

# =====================================================
# SESSION FACTORY
# =====================================================
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
Base = declarative_base()

# =====================================================
# DATABASE DEPENDENCY
# =====================================================
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# =====================================================
# DATABASE INITIALIZER
# =====================================================
async def init_db():
    try:
        async with engine.begin() as conn:
            import app.models
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"⚠️ Database init failed: {e}")