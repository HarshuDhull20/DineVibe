from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum

from app.models.user import UserRole


# ---------------------------------------------------------
# ENUMS
# ---------------------------------------------------------

class LoginMethod(str, Enum):
    PASSWORD = "password"
    OTP = "otp"


class AuthStatus(str, Enum):
    FIRST_LOGIN = "FIRST_LOGIN"
    MFA_REQUIRED = "MFA_REQUIRED"
    SUCCESS = "SUCCESS"


# ---------------------------------------------------------
# REGISTER
# ---------------------------------------------------------

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr
    phone_number: Optional[str] = Field(
        None, pattern=r"^\+?[1-9]\d{9,14}$"
    )
    password: str = Field(..., min_length=8)
    role: UserRole

    class Config:
        json_schema_extra = {
            "example": {
                "username": "harshu",
                "email": "harshudhull46@gmail.com",
                "password": "StrongPass123",
                "role": "normal_user"
            }
        }


# ---------------------------------------------------------
# PASSWORD LOGIN (STEP 1)
# ---------------------------------------------------------

class PasswordLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "harshudhull46@gmail.com",
                "password": "StrongPass123"
            }
        }


# ---------------------------------------------------------
# AUTH FLOW RESPONSE (NEW – IMPORTANT)
# ---------------------------------------------------------

class AuthFlowResponse(BaseModel):
    status: AuthStatus
    access_token: Optional[str] = None      # Only if SUCCESS
    temp_token: Optional[str] = None        # For MFA / password setup
    role: Optional[str] = None
    mfa_required: bool = False
    mfa_setup_required: bool = False
    must_change_password: bool = False


# ---------------------------------------------------------
# OTP VERIFY (STEP 2)
# ---------------------------------------------------------

class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=4, max_length=6)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "harshudhull46@gmail.com",
                "otp": "123456"
            }
        }


# ---------------------------------------------------------
# SET PASSWORD (NEW)
# ---------------------------------------------------------

class SetPasswordRequest(BaseModel):
    email: EmailStr
    new_password: str = Field(..., min_length=8)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "harshudhull46@gmail.com",
                "new_password": "NewStrongPass123"
            }
        }


# ---------------------------------------------------------
# FINAL TOKEN RESPONSE (Only used after complete login)
# ---------------------------------------------------------

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


# ---------------------------------------------------------
# FORGOT PASSWORD
# ---------------------------------------------------------

class ForgotPasswordRequest(BaseModel):
    email: EmailStr


# ---------------------------------------------------------
# RESET PASSWORD
# ---------------------------------------------------------

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=4, max_length=6)
    new_password: str = Field(..., min_length=8)
