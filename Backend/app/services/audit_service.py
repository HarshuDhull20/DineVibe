from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from datetime import datetime

from app.models.audit_log import AuditLog


# =========================================================
# CREATE AUDIT LOG
# =========================================================
async def create_audit_log(
    db: AsyncSession,
    user_id: int,
    action: str,
    details: Optional[str] = None
):
    """
    Creates a new audit log entry.

    Used for:
    - Login / Logout
    - Password change
    - Role change
    - Account deactivation
    - MFA changes
    - Admin actions
    """

    log = AuditLog(
        user_id=user_id,
        action=action,
        details=details,
        timestamp=datetime.utcnow()
    )

    db.add(log)
    await db.commit()
    await db.refresh(log)

    return log


# =========================================================
# FETCH USER AUDIT LOGS
# =========================================================
async def get_user_audit_logs(
    db: AsyncSession,
    user_id: int,
    limit: int = 50
) -> List[AuditLog]:
    """
    Returns audit logs for a specific user.

    Feature mapping:
    - Login history visibility
    - Security activity log
    """

    result = await db.execute(
        select(AuditLog)
        .where(AuditLog.user_id == user_id)
        .order_by(AuditLog.timestamp.desc())
        .limit(limit)
    )

    return result.scalars().all()


# =========================================================
# FETCH SYSTEM-WIDE AUDIT LOGS (ADMIN)
# =========================================================
async def get_system_audit_logs(
    db: AsyncSession,
    limit: int = 100
) -> List[AuditLog]:
    """
    Returns audit logs for the entire system.

    Feature mapping:
    - Admin audit dashboard
    - Role approval workflow
    - Security monitoring
    """

    result = await db.execute(
        select(AuditLog)
        .order_by(AuditLog.timestamp.desc())
        .limit(limit)
    )

    return result.scalars().all()


# =========================================================
# HELPER METHODS FOR COMMON EVENTS
# =========================================================

async def log_login_success(db: AsyncSession, user_id: int):
    await create_audit_log(
        db=db,
        user_id=user_id,
        action="LOGIN_SUCCESS",
        details="User logged in successfully"
    )


async def log_login_failure(db: AsyncSession, user_id: Optional[int]):
    # user_id can be None if user does not exist
    await create_audit_log(
        db=db,
        user_id=user_id or 0,
        action="LOGIN_FAILURE",
        details="Failed login attempt"
    )


async def log_password_change(db: AsyncSession, user_id: int):
    await create_audit_log(
        db=db,
        user_id=user_id,
        action="PASSWORD_CHANGE",
        details="User changed password"
    )


async def log_role_change(
    db: AsyncSession,
    user_id: int,
    old_role: str,
    new_role: str
):
    await create_audit_log(
        db=db,
        user_id=user_id,
        action="ROLE_CHANGE",
        details=f"Role changed from {old_role} to {new_role}"
    )


async def log_account_status_change(
    db: AsyncSession,
    user_id: int,
    is_active: bool
):
    await create_audit_log(
        db=db,
        user_id=user_id,
        action="ACCOUNT_STATUS_CHANGE",
        details=f"Account {'activated' if is_active else 'deactivated'}"
    )


async def log_mfa_status_change(
    db: AsyncSession,
    user_id: int,
    enabled: bool
):
    await create_audit_log(
        db=db,
        user_id=user_id,
        action="MFA_STATUS_CHANGE",
        details=f"MFA {'enabled' if enabled else 'disabled'}"
    )


async def log_admin_action(
    db: AsyncSession,
    admin_id: int,
    target_user_id: int,
    action: str,
    details: str
):
    await create_audit_log(
        db=db,
        user_id=admin_id,
        action=f"ADMIN_{action}",
        details=f"Target User ID {target_user_id}: {details}"
    )
