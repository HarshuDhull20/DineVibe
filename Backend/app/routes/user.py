from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import List
from app.database.db import get_db
from app.dependencies.auth import get_current_user
#from app.dependencies.roles import require_roles
from app.models.user import User, UserRole
from app.models.session import UserSession
from app.models.audit_log import AuditLog
from app.schemas.user import (
    UserProfileResponse,
    SessionResponse,
    PasswordChangeRequest
)
from app.core.security import verify_password, hash_password

router = APIRouter(
    prefix="/user",
    tags=["User Profile & Sessions"]
)

# ---------------------------------------------------------
# GET CURRENT USER PROFILE + PERMISSIONS
# ---------------------------------------------------------
@router.get("/me", response_model=UserProfileResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Features:
    - Role-based identity
    - Permissions visibility (Swagger proof)
    - Transparency to user
    """
    permissions_map = {
    UserRole.SUPER_ADMIN: ["full_platform_control"],
    UserRole.ADMIN: ["admin_control"],
    UserRole.RESTAURANT_OWNER: ["manage_restaurant", "invite_staff", "view_analytics"],
    UserRole.RESTAURANT_STAFF: ["process_orders", "manage_menu"],
    UserRole.NORMAL_USER: ["browse_restaurants", "view_menu", "write_review"],
    UserRole.INFLUENCER: ["create_campaign", "view_earnings"],
    }

    return {
        "id": current_user.id,
        "email": current_user.email,
        "phone": current_user.phone_number,
        "role": current_user.role,
        "permissions": permissions_map.get(current_user.role, []),
        "is_active": current_user.is_active,
        "is_mfa_enabled": current_user.is_mfa_enabled,
        "last_login": current_user.last_login
    }


# ---------------------------------------------------------
# LIST ACTIVE SESSIONS (MULTI-DEVICE)
# ---------------------------------------------------------
@router.get("/sessions", response_model=List[SessionResponse])
async def get_my_sessions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Features:
    - Multi-device login
    - Device-wise session listing
    """

    result = await db.execute(
        select(UserSession).where(
            UserSession.user_id == current_user.id,
            UserSession.is_active == True
        )
    )
    return result.scalars().all()


# ---------------------------------------------------------
# LOGOUT FROM A SPECIFIC DEVICE
# ---------------------------------------------------------
@router.post("/sessions/{session_id}/logout")
async def logout_specific_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Features:
    - Logout from specific device
    """

    result = await db.execute(
        select(UserSession).where(
            UserSession.id == session_id,
            UserSession.user_id == current_user.id
        )
    )
    session = result.scalars().first()

    if not session:
        raise HTTPException(404, "Session not found")

    session.is_active = False

    audit = AuditLog(
        user_id=current_user.id,
        action="LOGOUT_DEVICE",
        details=f"Logged out from device {session.device_name}"
    )

    db.add(audit)
    await db.commit()

    return {"message": "Logged out from device successfully"}


# ---------------------------------------------------------
# GLOBAL LOGOUT (ALL DEVICES)
# ---------------------------------------------------------
@router.post("/logout-all")
async def logout_all_sessions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Features:
    - Global logout
    - Security control
    """

    await db.execute(
        update(UserSession)
        .where(UserSession.user_id == current_user.id)
        .values(is_active=False)
    )

    audit = AuditLog(
        user_id=current_user.id,
        action="LOGOUT_ALL",
        details="User logged out from all devices"
    )

    db.add(audit)
    await db.commit()

    return {"message": "Logged out from all devices"}


# ---------------------------------------------------------
# CHANGE PASSWORD
# ---------------------------------------------------------
@router.post("/change-password")
async def change_password(
    payload: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    if not verify_password(payload.old_password, current_user.hashed_password):
        raise HTTPException(400, "Old password is incorrect")

    # ==========================================
    # PASSWORD REUSE PREVENTION
    # ==========================================
    history_result = await db.execute(
        select(PasswordHistory)
        .where(PasswordHistory.user_id == current_user.id)
        .order_by(PasswordHistory.created_at.desc())
        .limit(5)
    )

    history_entries = history_result.scalars().all()

    for entry in history_entries:
        if verify_password(payload.new_password, entry.password_hash):
            raise HTTPException(
                status_code=400,
                detail="You cannot reuse your last 5 passwords"
            )

    # Store current password into history
    db.add(
        PasswordHistory(
            user_id=current_user.id,
            password_hash=current_user.hashed_password
        )
    )

    # Set new password
    current_user.hashed_password = hash_password(payload.new_password)
    current_user.password_changed_at = datetime.utcnow()

    audit = AuditLog(
        user_id=current_user.id,
        action="PASSWORD_CHANGED",
        details="User changed password"
    )

    db.add(audit)
    await db.commit()

    return {"message": "Password updated successfully"}

# ---------------------------------------------------------
# SELF DEACTIVATE ACCOUNT
# ---------------------------------------------------------
@router.post("/deactivate")
async def deactivate_my_account(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Features:
    - Account deactivation
    - User control
    """

    current_user.is_active = False

    await db.execute(
        update(UserSession)
        .where(UserSession.user_id == current_user.id)
        .values(is_active=False)
    )

    audit = AuditLog(
        user_id=current_user.id,
        action="ACCOUNT_DEACTIVATED",
        details="User deactivated own account"
    )

    db.add(audit)
    await db.commit()

    return {"message": "Account deactivated successfully"}
from app.models.password_history import PasswordHistory