from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.models.mfa import MFAType, MFAPurpose


# =========================================================
# ENABLE MFA
# =========================================================

class EnableMFARequest(BaseModel):
    mfa_type: MFAType


class EnableMFAResponse(BaseModel):
    mfa_type: MFAType
    secret: Optional[str] = None
    qr_code_url: Optional[str] = None


# =========================================================
# VERIFY MFA
# =========================================================

class VerifyMFARequest(BaseModel):
    code: str = Field(..., min_length=4, max_length=8)
    purpose: MFAPurpose


class VerifyMFAResponse(BaseModel):
    verified: bool
    message: str


# =========================================================
# DISABLE MFA
# =========================================================

class DisableMFARequest(BaseModel):
    mfa_type: MFAType


# =========================================================
# MFA STATUS (THIS WAS MISSING)
# =========================================================

class MFAStatusResponse(BaseModel):
    """
    Returned when checking MFA status
    """

    is_enabled: bool
    mfa_type: Optional[MFAType] = None
    enabled_at: Optional[datetime] = None


# =========================================================
# MFA DEVICE RESPONSE
# =========================================================

class MFADeviceResponse(BaseModel):
    id: int
    mfa_type: MFAType
    is_active: bool
    created_at: datetime
    last_used_at: Optional[datetime]

    class Config:
        from_attributes = True


# =========================================================
# MFA CHALLENGE RESPONSE (ADMIN / DEBUG)
# =========================================================

class MFAChallengeResponse(BaseModel):
    id: int
    mfa_type: MFAType
    purpose: MFAPurpose
    is_verified: bool
    expires_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True
