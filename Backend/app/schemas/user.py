from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List, Dict
from datetime import datetime
from app.models.user import UserRole


# =========================================================
# BASE USER SCHEMA (SHARED)
# =========================================================
class UserBase(BaseModel):
    """
    Shared fields across user-related schemas
    """

    username: str = Field(
        ..., min_length=3, max_length=50,
        description="Unique username across the platform"
    )

    email: Optional[EmailStr] = Field(
        None, description="Email address (optional for OTP-based users)"
    )

    phone_number: Optional[str] = Field(
        None, description="Phone number with country code"
    )

    role: UserRole = Field(
        ..., description="Role of the user in the system"
    )

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, value):
        if value and not value.startswith("+"):
            raise ValueError("Phone number must include country code (e.g. +91)")
        return value


# =========================================================
# USER REGISTRATION
# =========================================================
class UserCreate(UserBase):
    """
    Used during registration
    """

    password: Optional[str] = Field(
        None,
        min_length=8,
        description="Password (optional for OTP / Social login users)"
    )

    accept_terms: bool = Field(
        ..., description="User must accept terms & privacy policy"
    )

    @field_validator("accept_terms")
    @classmethod
    def terms_must_be_accepted(cls, v):
        if not v:
            raise ValueError("Terms and Privacy Policy must be accepted")
        return v


# =========================================================
# USER RESPONSE (ME / PROFILE)
# =========================================================
class UserOut(UserBase):
    """
    Returned to frontend (/me, admin panels)
    """

    id: int

    # --- Account Status ---
    is_active: bool = Field(
        ..., description="Account active or deactivated"
    )

    is_mfa_enabled: bool = Field(
        ..., description="Is MFA enabled for this user"
    )

    # --- Security Metadata ---
    last_login: Optional[datetime]
    created_at: datetime

    # --- Sessions & Access ---
    permissions: List[str] = Field(
        default=[],
        description="Computed permissions based on role"
    )

    # --- Role Metadata ---
    role_metadata: Optional[Dict] = Field(
        None,
        description="Extra role-specific data (sub-roles, partner roles, etc.)"
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 12,
                "username": "rahul_k",
                "email": "rahul@test.com",
                "phone_number": "+919876543210",
                "role": "restaurant_owner",
                "is_active": True,
                "is_mfa_enabled": True,
                "last_login": "2026-02-08T18:20:00Z",
                "created_at": "2026-01-01T10:00:00Z",
                "permissions": [
                    "manage_restaurant",
                    "invite_staff",
                    "view_analytics"
                ],
                "role_metadata": {
                    "sub_role": "manager",
                    "partner": "OpenTable"
                }
            }
        }


# ALIAS REQUIRED BY ROUTES
UserProfileResponse = UserOut


# =========================================================
# USER UPDATE (PROFILE)
# =========================================================
class UserUpdate(BaseModel):
    """
    Used to update profile details
    """

    email: Optional[EmailStr]
    phone_number: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "email": "newmail@test.com",
                "phone_number": "+919999999999"
            }
        }


# =========================================================
# ACCOUNT STATUS MANAGEMENT
# =========================================================
class UserStatusUpdate(BaseModel):
    """
    Used for admin / self-deactivation
    """

    is_active: bool = Field(
        ..., description="Activate or deactivate account"
    )

    reason: Optional[str] = Field(
        None, description="Reason for deactivation"
    )


# =========================================================
# ROLE CHANGE / UPGRADE
# =========================================================
class RoleUpgradeRequest(BaseModel):
    """
    User requesting role upgrade
    """

    requested_role: UserRole
    reason: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "requested_role": "influencer",
                "reason": "I want to run campaigns"
            }
        }


class RoleUpgradeResponse(BaseModel):
    message: str
    current_role: UserRole
    requested_role: UserRole
    status: str  # pending / approved / rejected


# =========================================================
# PASSWORD & SECURITY
# =========================================================
class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)

    class Config:
        json_schema_extra = {
            "example": {
                "old_password": "Old@12345",
                "new_password": "New@12345"
            }
        }


class AccountDeactivate(BaseModel):
    """
    Self-deactivation request
    """

    confirm: bool = Field(
        ..., description="Must be true to confirm deactivation"
    )


# =========================================================
# ADMIN VIEW (USER LISTING)
# =========================================================
class AdminUserListOut(BaseModel):
    """
    Used in admin dashboards
    """

    id: int
    username: str
    role: UserRole
    is_active: bool
    last_login: Optional[datetime]

    class Config:
        from_attributes = True
# =========================================================
# SESSION RESPONSE
# =========================================================
class SessionResponse(BaseModel):
    """
    Returned when listing active user sessions
    """

    id: int
    device_type: str
    device_name: Optional[str]
    ip_address: str
    location: Optional[str]
    is_active: bool
    last_activity_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True
# ALIAS REQUIRED BY ROUTES
PasswordChangeRequest = PasswordChange
