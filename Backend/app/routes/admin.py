from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database.db import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.permission import require_permission
from app.models.user import User, UserRole
from app.models.session import UserSession
from app.models.audit_log import AuditLog
from app.schemas.admin import (
    UserStatusUpdate,
    RoleApprovalRequest,
    AuditLogOut,
    UserOut
)

router = APIRouter(
    prefix="/admin",
    tags=["Super Admin"],
)

# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------
@router.get("/health")
async def admin_health(
    user: User = Depends(require_permission("VIEW_AUDIT_LOGS"))
):
    return {
        "status": "Admin panel active",
        "checked_by": user.username
    }


# ---------------------------------------------------------
# ACTIVATE / DEACTIVATE USER
# ---------------------------------------------------------
@router.patch("/users/{user_id}/status", response_model=UserOut)
async def change_user_status(
    user_id: int,
    payload: UserStatusUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_permission("UPDATE_SETTINGS"))
):

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id == admin.id:
        raise HTTPException(
            status_code=400,
            detail="You cannot deactivate your own account"
        )

    user.is_active = payload.is_active

    audit = AuditLog(
        user_id=user.id,
        action="ACCOUNT_STATUS_CHANGE",
        details=f"{'Activated' if payload.is_active else 'Deactivated'} by {admin.username}",
    )
    db.add(audit)

    await db.commit()
    await db.refresh(user)

    return user


# ---------------------------------------------------------
# ROLE APPROVAL / ROLE CHANGE
# ---------------------------------------------------------
@router.post("/users/{user_id}/approve-role")
async def approve_role(
    user_id: int,
    payload: RoleApprovalRequest,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_permission("MANAGE_STAFF"))
):

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id == admin.id:
        raise HTTPException(
            status_code=400,
            detail="You cannot change your own role"
        )

    old_role = user.role
    user.role = payload.new_role

    audit = AuditLog(
        user_id=user.id,
        action="ROLE_CHANGE",
        details=f"{old_role} → {payload.new_role} by {admin.username}"
    )

    db.add(audit)
    await db.commit()

    return {
        "message": "Role updated successfully",
        "user_id": user.id,
        "old_role": old_role,
        "new_role": payload.new_role
    }


# ---------------------------------------------------------
# FORCE LOGOUT (ALL DEVICES)
# ---------------------------------------------------------
@router.post("/users/{user_id}/force-logout")
async def force_logout_all_sessions(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_permission("MANAGE_STAFF"))
):

    result = await db.execute(
        select(UserSession).where(
            UserSession.user_id == user_id,
            UserSession.is_active == True
        )
    )
    sessions = result.scalars().all()

    for session in sessions:
        session.is_active = False

    audit = AuditLog(
        user_id=user_id,
        action="FORCE_LOGOUT",
        details=f"All sessions revoked by {admin.username}"
    )
    db.add(audit)

    await db.commit()

    return {
        "message": f"All active sessions revoked for user {user_id}"
    }


# ---------------------------------------------------------
# VIEW AUDIT LOGS
# ---------------------------------------------------------
@router.get("/audit-logs", response_model=List[AuditLogOut])
async def get_audit_logs(
    limit: int = Query(50, le=200),
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_permission("VIEW_AUDIT_LOGS"))
):

    result = await db.execute(
        select(AuditLog)
        .order_by(AuditLog.timestamp.desc())
        .limit(limit)
    )

    return result.scalars().all()


# ---------------------------------------------------------
# LIST USERS
# ---------------------------------------------------------
@router.get("/users", response_model=List[UserOut])
async def list_users(
    role: UserRole | None = None,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_permission("VIEW_AUDIT_LOGS"))
):

    query = select(User)

    if role:
        query = query.where(User.role == role)

    result = await db.execute(query)
    return result.scalars().all()
