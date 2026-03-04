from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.database.base import AsyncSessionLocal

# =====================================================
# DATABASE SESSION PROVIDER
# =====================================================

async def get_db():
    """
    Provides a transactional async database session
    for each API request.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database transaction failed",
            )
        finally:
            await session.close()

# =====================================================
# DATABASE TRANSACTION HELPERS
# =====================================================

async def commit_or_rollback(session: AsyncSession):
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise

async def flush_and_refresh(session: AsyncSession, instance):
    try:
        await session.flush()
        await session.refresh(instance)
    except Exception:
        await session.rollback()
        raise
