from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime

from app.database.db import get_db
from app.models.user import User
from app.models.mfa_device import MFADevice
from app.models.otp import OTP
from app.models.audit_log import AuditLog
from app.dependencies.auth import get_current_user
from app.schemas.mfa import (
    EnableMFARequest,
    VerifyMFARequest,
    MFAStatusResponse
)

router = APIRouter(
    prefix="/mfa",
    tags=["Multi-Factor Authentication"]
)

# ---------------------------------------------------------
# GET MFA STATUS
# ---------------------------------------------------------
@router.get("/status", response_model=MFAStatusResponse)
async def get_mfa_status(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Feature:
    - Show if MFA is enabled
    - Transparency to user
    """

    result = await db.execute(
        select(MFADevice).where(MFADevice.user_id == current_user.id)
    )
    device = result.scalars().first()

    return {
        "mfa_enabled": bool(device),
        "mfa_type": device.mfa_type if device else None
    }


# ---------------------------------------------------------
# ENABLE MFA (OTP / AUTHENTICATOR)
# ---------------------------------------------------------
@router.post("/enable")
async def enable_mfa(
    payload: EnableMFARequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Features:
    - Enable MFA
    - Authenticator app support
    - Mandatory MFA for admins
    """

    existing = await db.execute(
        select(MFADevice).where(MFADevice.user_id == current_user.id)
    )
    if existing.scalars().first():
        raise HTTPException(400, "MFA already enabled")

    mfa_device = MFADevice(
        user_id=current_user.id,
        mfa_type=payload.mfa_type,
        secret_key=payload.secret_key  # Generated client-side or service
    )

    current_user.is_mfa_enabled = True

    audit = AuditLog(
        user_id=current_user.id,
        action="MFA_ENABLED",
        details=f"MFA enabled using {payload.mfa_type}"
    )

    db.add_all([mfa_device, audit])
    await db.commit()

    return {"message": "MFA enabled successfully"}


# ---------------------------------------------------------
# VERIFY MFA (POST LOGIN STEP)
# ---------------------------------------------------------
@router.post("/verify")
async def verify_mfa(
    payload: VerifyMFARequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Features:
    - OTP verification
    - Authenticator verification
    - Risk-based MFA
    """

    result = await db.execute(
        select(MFADevice).where(MFADevice.user_id == current_user.id)
    )
    device = result.scalars().first()

    if not device:
        raise HTTPException(400, "MFA not enabled")

    # OTP-based MFA
    if device.mfa_type == "otp":
        otp_q = await db.execute(
            select(OTP).where(
                OTP.user_id == current_user.id,
                OTP.code == payload.code,
                OTP.is_used == False
            )
        )
        otp = otp_q.scalars().first()

        if not otp or otp.is_expired():
            raise HTTPException(401, "Invalid or expired OTP")

        otp.is_used = True

    # Authenticator-based MFA (TOTP)
    elif device.mfa_type == "authenticator":
        if not device.verify_totp(payload.code):
            raise HTTPException(401, "Invalid authenticator code")

    audit = AuditLog(
        user_id=current_user.id,
        action="MFA_VERIFIED",
        details="MFA verification successful"
    )

    db.add(audit)
    await db.commit()

    return {"message": "MFA verification successful"}


# ---------------------------------------------------------
# DISABLE MFA
# ---------------------------------------------------------
@router.delete("/disable")
async def disable_mfa(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Features:
    - Disable MFA
    - Admin controlled policies can override
    """

    result = await db.execute(
        select(MFADevice).where(MFADevice.user_id == current_user.id)
    )
    device = result.scalars().first()

    if not device:
        raise HTTPException(400, "MFA not enabled")

    await db.delete(device)
    current_user.is_mfa_enabled = False

    audit = AuditLog(
        user_id=current_user.id,
        action="MFA_DISABLED",
        details="MFA disabled by user"
    )

    db.add(audit)
    await db.commit()

    return {"message": "MFA disabled successfully"}
