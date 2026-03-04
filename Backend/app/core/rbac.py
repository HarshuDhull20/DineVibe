# app/core/rbac.py

from fastapi import Depends, HTTPException, status
from app.dependencies.auth import get_current_user
from app.models.user import User


# ==================================
# Permission Matrix
# ==================================

ROLE_PERMISSIONS = {

    "normal_user": [
        "view_restaurants",
        "book_reservation",
        "view_profile"
    ],

    "restaurant_owner": [
        "manage_reservations",
        "manage_staff",
        "view_analytics",
        "manage_restaurant"
    ],

    "restaurant_staff": [
        "process_reservations",
        "view_reservations"
    ],

    "influencer": [
        "create_campaign",
        "view_campaign_stats"
    ],

    "super_admin": [
        "all_permissions"
    ]
}


# ==================================
# Role Checker Dependency
# ==================================

def require_role(allowed_roles: list[str]):

    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role.value not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: role not authorized"
            )
        return current_user

    return role_checker


# ==================================
# Permission Checker Dependency
# ==================================

def require_permission(permission: str):

    def permission_checker(current_user: User = Depends(get_current_user)):

        role = current_user.role.value

        if role == "super_admin":
            return current_user

        allowed_permissions = ROLE_PERMISSIONS.get(role, [])

        if permission not in allowed_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: insufficient permission"
            )

        return current_user

    return permission_checker
