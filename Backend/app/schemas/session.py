from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ---------------------------------------------------------
# SESSION RESPONSE (USER / ADMIN VIEW)
# ---------------------------------------------------------
class SessionOut(BaseModel):
    """
    Returned when listing active sessions
    (User dashboard / Admin view)
    """

    id: int
    device_type: str = Field(
        ..., description="web | mobile"
    )
    device_name: Optional[str] = Field(
        None, description="Chrome on Windows, iPhone 15, etc."
    )
    ip_address: str
    location: Optional[str] = Field(
        None, description="City / Country derived from IP"
    )
    is_active: bool
    last_activity: datetime
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 12,
                "device_type": "mobile",
                "device_name": "iPhone 15",
                "ip_address": "103.21.45.10",
                "location": "Hyderabad, India",
                "is_active": True,
                "last_activity": "2026-02-08T18:45:12Z",
                "created_at": "2026-02-08T17:00:00Z"
            }
        }


# ---------------------------------------------------------
# CREATE SESSION (INTERNAL USE)
# ---------------------------------------------------------
class SessionCreate(BaseModel):
    """
    Used internally when creating a new session
    after login / OTP verification
    """

    user_id: int
    device_type: str = Field(..., description="web | mobile")
    device_name: Optional[str]
    ip_address: str
    location: Optional[str]
    refresh_token: str

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 5,
                "device_type": "web",
                "device_name": "Chrome on Windows",
                "ip_address": "49.37.210.15",
                "location": "Bangalore, India",
                "refresh_token": "uuid-refresh-token"
            }
        }


# ---------------------------------------------------------
# LOGOUT FROM A SINGLE DEVICE
# ---------------------------------------------------------
class SessionTerminateRequest(BaseModel):
    """
    Used when user wants to logout from a specific device
    """

    session_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": 12
            }
        }


class SessionTerminateResponse(BaseModel):
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Session terminated successfully"
            }
        }


# ---------------------------------------------------------
# FORCE LOGOUT (ADMIN / SECURITY)
# ---------------------------------------------------------
class ForceLogoutResponse(BaseModel):
    """
    Used for:
    - Global logout
    - Admin forced logout
    """

    terminated_sessions: int
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "terminated_sessions": 3,
                "message": "All active sessions terminated"
            }
        }


# ---------------------------------------------------------
# SESSION SECURITY METADATA (OPTIONAL)
# ---------------------------------------------------------
class SessionSecurityInfo(BaseModel):
    """
    Used internally for security analysis
    """

    ip_address: str
    location: Optional[str]
    user_agent: Optional[str]
    is_suspicious: bool = False
    risk_reason: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "ip_address": "103.21.45.10",
                "location": "Unknown",
                "user_agent": "Mozilla/5.0",
                "is_suspicious": True,
                "risk_reason": "New country detected"
            }
        }
