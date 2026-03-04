from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime


# ---------------------------------------------------------
# ENUMS
# ---------------------------------------------------------
class OTPPurpose(str, Enum):
    LOGIN = "login"
    SIGNUP = "signup"
    PASSWORD_RESET = "password_reset"
    ACCOUNT_RECOVERY = "account_recovery"
    MFA_VERIFICATION = "mfa_verification"


class OTPChannel(str, Enum):
    SMS = "sms"
    EMAIL = "email"


# ---------------------------------------------------------
# SEND OTP
# ---------------------------------------------------------
class OTPSendRequest(BaseModel):
    """
    Used when user requests an OTP
    """

    phone_number: Optional[str] = Field(
        None, description="Phone number with country code"
    )
    email: Optional[str] = Field(
        None, description="Email address"
    )
    purpose: OTPPurpose
    channel: OTPChannel

    class Config:
        json_schema_extra = {
            "example": {
                "phone_number": "+919876543210",
                "purpose": "login",
                "channel": "sms"
            }
        }


class OTPSendResponse(BaseModel):
    """
    Returned after OTP is generated
    """

    message: str
    expires_in_seconds: int
    resend_available_in_seconds: int

    class Config:
        json_schema_extra = {
            "example": {
                "message": "OTP sent successfully",
                "expires_in_seconds": 300,
                "resend_available_in_seconds": 30
            }
        }


# ---------------------------------------------------------
# VERIFY OTP
# ---------------------------------------------------------
class OTPVerifyRequest(BaseModel):
    """
    Used when user submits OTP
    """

    otp_code: str = Field(..., min_length=6, max_length=6)
    phone_number: Optional[str] = None
    email: Optional[str] = None
    purpose: OTPPurpose

    class Config:
        json_schema_extra = {
            "example": {
                "otp_code": "123456",
                "phone_number": "+919876543210",
                "purpose": "login"
            }
        }


class OTPVerifyResponse(BaseModel):
    """
    Returned after OTP verification
    """

    verified: bool
    message: str
    verified_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "verified": True,
                "message": "OTP verified successfully",
                "verified_at": "2026-02-08T14:10:00Z"
            }
        }


# ---------------------------------------------------------
# RESEND OTP
# ---------------------------------------------------------
class OTPResendRequest(BaseModel):
    """
    Used when user requests OTP resend
    """

    phone_number: Optional[str] = None
    email: Optional[str] = None
    purpose: OTPPurpose
    channel: OTPChannel

    class Config:
        json_schema_extra = {
            "example": {
                "phone_number": "+919876543210",
                "purpose": "login",
                "channel": "sms"
            }
        }


# ---------------------------------------------------------
# OTP STATUS (OPTIONAL – FOR DEBUG / ADMIN)
# ---------------------------------------------------------
class OTPStatusResponse(BaseModel):
    """
    Used internally or for admin debugging
    """

    is_used: bool
    expires_at: datetime
    attempts_left: int

    class Config:
        json_schema_extra = {
            "example": {
                "is_used": False,
                "expires_at": "2026-02-08T14:15:00Z",
                "attempts_left": 3
            }
        }
