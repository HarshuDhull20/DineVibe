from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from app.models.user import User
from app.models.session import UserSession
from app.core.security import verify_password, hash_password


# =========================================================
# AUTHENTICATE USER (PASSWORD CHECK ONLY)
# =========================================================
async def authenticate_user(
    db: AsyncSession,
    email: str,
    password: str
):
    """
    Basic credential validation.
    Does NOT issue tokens.
    Does NOT create sessions.
    Used by routes/auth.py.
    """

    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account deactivated")

    return user


# =========================================================
# UPDATE USER PASSWORD
# =========================================================
async def update_user_password(
    db: AsyncSession,
    user: User,
    new_password: str
):
    """
    Securely updates user password.
    """

    user.hashed_password = hash_password(new_password)
    user.must_change_password = False
    user.is_first_login = False

    await db.commit()
    await db.refresh(user)

    return user


# =========================================================
# CREATE SESSION (OPTIONAL)
# =========================================================
async def create_user_session(
    db: AsyncSession,
    user: User,
    access_token_jti: str,
    request
):
    """
    Creates a session entry after successful login.
    """

    session = UserSession(
        user_id=user.id,
        access_token_jti=access_token_jti,
        device_type="web",
        device_name=request.headers.get("user-agent"),
        ip_address=request.client.host if request.client else None,
        is_active=True,
        last_activity=datetime.now(timezone.utc)
    )

    db.add(session)
    await db.commit()

    return session