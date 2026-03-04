from fastapi import Depends, HTTPException, status
from typing import List, Dict

from app.auth import get_current_user
from app.models import User, UserRole


# =====================================================
# ROLE → PERMISSIONS MAPPING
# =====================================================
# This is the HEART of authorization in DineVibe

ROLE_PERMISSIONS: Dict[str, List[str]] = {

    # Normal Users (Customers)
    UserRole.NORMAL.value: [
        "browse_restaurants",
        "view_menu",
        "save_restaurant",
        "write_review",
        "manage_profile",
        "logout",
    ],

    #  Restaurant Owner
    UserRole.OWNER.value: [
        "manage_restaurant",
        "manage_menu",
        "view_orders",
        "manage_staff",
        "view_analytics",
        "invite_staff",
        "assign_roles",
        "logout",
    ],

    #  Restaurant Staff
    UserRole.STAFF.value: [
        "process_orders",
        "view_menu",
        "update_order_status",
        "logout",
    ],

    #  Influencer / Creator
    UserRole.INFLUENCER.value: [
        "create_campaign",
        "view_campaign_stats",
        "view_earnings",
        "withdraw_earnings",
        "logout",
    ],

    #  Super Admin
    UserRole.ADMIN.value: [
        "all_access",                
        "manage_users",
        "approve_roles",
        "view_audit_logs",
        "force_logout",
        "system_config",
    ],
}


# =====================================================
# PERMISSION CHECKER (Dependency)
# =====================================================
class PermissionChecker:
    """
    Dependency to enforce permission-based access control.

    Usage:
    Depends(PermissionChecker(["manage_restaurant"]))
    """

    def __init__(self, required_permissions: List[str]):
        self.required_permissions = required_permissions

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        user_role = (
            current_user.role.value
            if hasattr(current_user.role, "value")
            else str(current_user.role)
        )

        user_permissions = ROLE_PERMISSIONS.get(user_role, [])

        # Super Admin shortcut
        if "all_access" in user_permissions:
            return current_user

        for permission in self.required_permissions:
            if permission not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission '{permission}' required"
                )

        return current_user


# =====================================================
# HELPER FUNCTIONS (Used in Swagger / UI)
# =====================================================
def get_permissions_for_role(role: str) -> List[str]:
    """
    Used to show permissions in Swagger or /me API.
    """
    return ROLE_PERMISSIONS.get(role, [])


def is_action_allowed(user: User, action: str) -> bool:
    """
    Used internally for business logic checks.
    """
    role = user.role.value if hasattr(user.role, "value") else str(user.role)
    permissions = ROLE_PERMISSIONS.get(role, [])

    return "all_access" in permissions or action in permissions
