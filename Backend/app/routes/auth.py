from fastapi import APIRouter, Depends, HTTPException
import pyotp
from app.models.password_history import PasswordHistory
from sqlalchemy import select
from datetime import datetime, timedelta,timezone
import secrets
import string
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from typing import Literal

from app.database.db import get_db
from app.config.settings import settings
from app.models.user import User
from app.schemas.auth import (
    RegisterRequest,
    PasswordLoginRequest,
    OTPVerifyRequest,
    SetPasswordRequest
)
from app.core.security import (
    verify_password,
    hash_password,
    create_access_token
)
from app.services.otp_service import generate_mfa_otp, verify_mfa_otp

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/password")


# =========================================================
# UTIL — GENERATE TEMP PASSWORD
# =========================================================
def generate_temp_password():
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(10))


# =========================================================
# REGISTER
# =========================================================
@router.post("/register", status_code=201)
async def register_user(
    payload: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.email == payload.email)
    )

    if result.scalars().first():
        raise HTTPException(status_code=400, detail="User already exists")

    temp_password = generate_temp_password()

    user = User(
        username=payload.username,
        email=payload.email,
        phone_number=payload.phone_number,
        hashed_password=hash_password(temp_password),
        role=payload.role,
        is_active=True,
        is_mfa_enabled=False,
        must_change_password=True
    )

    db.add(user)
    await db.commit()

    return {
        "message": "User registered successfully",
        "temporary_password": temp_password
    }


# =========================================================
# PASSWORD LOGIN
# =========================================================
@router.post("/login/password")
async def password_login(
    payload: PasswordLoginRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.email == payload.email)
    )
    user = result.scalars().first()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account deactivated")
    
    # ==========================
    # PASSWORD EXPIRY CHECK
    # ==========================
    if user.password_changed_at and \
    user.password_changed_at < datetime.now(timezone.utc) - timedelta(days=90):
        return {"status": "PASSWORD_EXPIRED"}

    #  FORCE PASSWORD CHANGE AFTER MFA
    if user.must_change_password:
        return {
            "status": "MFA_REQUIRED",
            "available_methods": ["authenticator", "email", "sms"]
            }

    return {
        "status": "MFA_REQUIRED",
        "available_methods": ["authenticator", "email", "sms"]
    }


# =========================================================
# SELECT MFA METHOD
# =========================================================
class SelectMFARequest(BaseModel):
    email: EmailStr
    method: Literal["email", "authenticator", "sms"]


@router.post("/select-mfa")
async def select_mfa_method(
    payload: SelectMFARequest,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.email == payload.email)
    )
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.mfa_method = payload.method
    await db.commit()

    if payload.method == "email":
        otp_value = await generate_mfa_otp(db=db, user=user, method="email")
        return {
            "message": "Email OTP generated",
            "dev_otp" : otp_value
            }

    if payload.method == "sms":
        otp_value = await generate_mfa_otp(db=db, user=user,method="sms")
        return {
            "message": "SMS OTP generated",
            "dev_otp": otp_value  # REMOVE IN PRODUCTION
        }

    if payload.method == "authenticator":

        if not user.mfa_secret:
            user.mfa_secret = pyotp.random_base32()
            await db.commit()

        totp = pyotp.TOTP(user.mfa_secret)

        provisioning_url = totp.provisioning_uri(
            name=user.email,
            issuer_name="DineVibe"
        )

        return {
            "qr_url": provisioning_url,
            "manual_key": user.mfa_secret
        }

    raise HTTPException(status_code=400, detail="Invalid MFA method")


# =========================================================
# VERIFY OTP
# =========================================================
@router.post("/verify-otp")
async def verify_otp_route(
    payload: OTPVerifyRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.email == payload.email)
    )
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # ✅ DEMO BYPASS — accept 123456 for any user
    if payload.otp == "123456":
        user.is_mfa_enabled = True
        user.is_first_login = False
        await db.commit()

        if user.must_change_password:
            return {
                "status": "MFA_SETUP_COMPLETE",
                "must_change_password": True,
                "user": {
                    "name": user.name,
                    "email": user.email,
                    "role": user.role.value
                }
            }

        access_token, jti, expire = create_access_token(
            user_id=user.id,
            role=user.role.value,
            expires_delta=timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        )

        return {
            "status": "SUCCESS",
            "access_token": access_token,
            "user": {
                "name": user.name,
                "email": user.email,
                "role": user.role.value
            }
        }


    # AUTHENTICATOR FLOW
    if user.mfa_method == "authenticator":
        if not user.mfa_secret:
            raise HTTPException(status_code=400, detail="MFA not initialized")

        totp = pyotp.TOTP(user.mfa_secret)

        if not totp.verify(payload.otp):
            raise HTTPException(status_code=401, detail="Invalid verification code")

    else:
        await verify_mfa_otp(db=db, user=user, otp_code=payload.otp)

    # Mark MFA enabled
    user.is_mfa_enabled = True
    user.is_first_login = False

    await db.commit()

    # FIRST LOGIN FLOW
    if user.must_change_password:
        return {
            "status": "MFA_SETUP_COMPLETE",
            "must_change_password": True
        }

    # NORMAL LOGIN FLOW
    access_token, jti, expire = create_access_token(
        user_id=user.id,
        role=user.role.value,
        expires_delta=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    return {
        "status": "SUCCESS",
        "access_token": access_token,
        "role": user.role.value
    }


# =========================================================
# SET PASSWORD
# =========================================================
@router.post("/set-password")
async def set_password(
    payload: SetPasswordRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.email == payload.email)
    )
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ==========================================
    # PASSWORD REUSE PREVENTION (Last 5)
    # ==========================================
    history_result = await db.execute(
        select(PasswordHistory)
        .where(PasswordHistory.user_id == user.id)
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
    if user.hashed_password:
        db.add(
            PasswordHistory(
                user_id=user.id,
                password_hash=user.hashed_password
            )
        )

    # Set new password
    user.hashed_password = hash_password(payload.new_password)
    user.must_change_password = False
    user.password_changed_at = datetime.now(timezone.utc)

    access_token, jti, expire = create_access_token(
        user_id=user.id,
        role=user.role.value,
        expires_delta=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    await db.commit()

    return {
        "status": "SUCCESS",
        "access_token": access_token
    }