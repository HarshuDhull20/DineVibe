from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

from app.models.session import UserSession
from app.models.user import User
from app.services.audit_service import log_security_event
from app.config.settings import settings
import secrets


# =========================================================
# CREATE NEW SESSION (ON LOGIN)
# =========================================================
async def create_session(
    db: AsyncSession,
    user: User,
    device_type: str,
    device_name: str,
    ip_address: str,
    location: Optional[str] = None
) -> UserSession:
    """
    Creates a new login session for a user.
    """

    refresh_token = secrets.token_urlsafe(48)

    session = UserSession(
        user_id=user.id,
        refresh_token=refresh_token,
        device_type=device_type,
        device_name=device_name,
        ip_address=ip_address,
        location=location,
        is_active=True,
        last_activity=datetime.now(timezone.utc)
    )

    db.add(session)
    await db.commit()
    await db.refresh(session)

    await log_security_event(
        db,
        user.id,
        "SESSION_CREATED",
        f"New session on {device_name} ({device_type}) from IP {ip_address}"
    )

    return session


# =========================================================
# UPDATE SESSION ACTIVITY
# =========================================================
async def update_session_activity(
    db: AsyncSession,
    session: UserSession
):
    """
    Updates last activity timestamp.
    Called on every authenticated request.
    """
    session.last_activity = datetime.now(timezone.utc)
    await db.commit()


# =========================================================
# GET ALL ACTIVE SESSIONS FOR USER
# =========================================================
async def get_active_sessions(
    db: AsyncSession,
    user: User
):
    """
    Lists all active sessions for a user.
    """
    result = await db.execute(
        select(UserSession).where(
            UserSession.user_id == user.id,
            UserSession.is_active == True
        )
    )
    return result.scalars().all()


# =========================================================
# LOGOUT CURRENT SESSION
# =========================================================
async def logout_session(
    db: AsyncSession,
    session: UserSession
):
    """
    Logs out a single session.
    """
    session.is_active = False
    await db.commit()

    await log_security_event(
        db,
        session.user_id,
        "SESSION_LOGOUT",
        f"Logged out from device {session.device_name}"
    )


# =========================================================
# LOGOUT FROM SPECIFIC DEVICE
# =========================================================
async def logout_by_session_id(
    db: AsyncSession,
    user: User,
    session_id: int
):
    """
    Allows user/admin to logout from a specific device.
    """
    result = await db.execute(
        select(UserSession).where(
            UserSession.id == session_id,
            UserSession.user_id == user.id
        )
    )

    session = result.scalars().first()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    session.is_active = False
    await db.commit()

    await log_security_event(
        db,
        user.id,
        "SESSION_TERMINATED",
        f"Session ID {session_id} terminated manually"
    )


# =========================================================
# GLOBAL LOGOUT (ALL DEVICES)
# =========================================================
async def logout_all_sessions(
    db: AsyncSession,
    user: User,
    reason: str = "User initiated"
):
    """
    Logs out user from all devices.
    """
    result = await db.execute(
        select(UserSession).where(
            UserSession.user_id == user.id,
            UserSession.is_active == True
        )
    )

    sessions = result.scalars().all()

    for session in sessions:
        session.is_active = False

    await db.commit()

    await log_security_event(
        db,
        user.id,
        "GLOBAL_LOGOUT",
        f"All sessions terminated ({reason})"
    )


# =========================================================
# ADMIN FORCE LOGOUT
# =========================================================
async def admin_force_logout(
    db: AsyncSession,
    target_user_id: int,
    admin_id: int
):
    """
    Admin forcibly logs out a user from all devices.
    """
    result = await db.execute(
        select(UserSession).where(
            UserSession.user_id == target_user_id,
            UserSession.is_active == True
        )
    )

    sessions = result.scalars().all()

    for session in sessions:
        session.is_active = False

    await db.commit()

    await log_security_event(
        db,
        target_user_id,
        "ADMIN_FORCE_LOGOUT",
        f"Admin ID {admin_id} terminated all sessions"
    )


# =========================================================
# STAFF SESSION ISOLATION CHECK
# =========================================================
def enforce_staff_session_isolation(user: User):
    """
    Ensures staff sessions are isolated per restaurant.
    (Hook for future restaurant-based restrictions)
    """
    if user.role.value == "restaurant_staff":
        # Placeholder for restaurant-specific checks
        pass
