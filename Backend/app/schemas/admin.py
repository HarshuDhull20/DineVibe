from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.models.user import UserRole


# =========================================================
# ADMIN: USER LISTING
# =========================================================
class AdminUserOut(BaseModel):
    id: int
    username: str
    email: Optional[str]
    phone_number: Optional[str]
    role: UserRole
    is_active: bool
    is_mfa_enabled: bool
    last_login: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


# =========================================================
# ADMIN: UPDATE USER STATUS
# =========================================================
class AdminUserStatusUpdate(BaseModel):
    is_active: bool = Field(..., description="Activate or deactivate user")
    reason: Optional[str] = Field(None, description="Reason for action")


# =========================================================
# ADMIN: ROLE CHANGE / APPROVAL
# =========================================================
class AdminRoleChangeRequest(BaseModel):
    new_role: UserRole
    reason: Optional[str] = None


# =========================================================
# ADMIN: BULK ROLE CHANGE
# =========================================================
class AdminBulkRoleChangeRequest(BaseModel):
    user_ids: List[int]
    new_role: UserRole
    reason: Optional[str] = None


# =========================================================
# ADMIN: AUDIT LOG OUTPUT
# =========================================================
class AuditLogOut(BaseModel):
    id: int
    user_id: int
    action: str
    details: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# =========================================================
# ADMIN: GENERIC RESPONSE
# =========================================================
class AdminActionResponse(BaseModel):
    message: str


# =========================================================
#  ALIASES REQUIRED BY ROUTES
# =========================================================
UserStatusUpdate = AdminUserStatusUpdate
RoleApprovalRequest = AdminRoleChangeRequest


# =========================================================
#  RE-EXPORT USER SCHEMA FOR ADMIN ROUTES
# =========================================================
from app.schemas.user import UserOut
