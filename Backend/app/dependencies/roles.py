from fastapi import Depends, HTTPException, status
from typing import Callable

from app.models.user import User, UserRole
from app.dependencies.auth import get_current_user

# =====================================================
# GENERIC ROLE CHECKER (STRICT ROLE MATCH)
# =====================================================

class RequireRoles:
    """
    Dependency to enforce strict role-based access.
    Example:
        Depends(RequireRoles(UserRole.ADMIN))
        Depends(RequireRoles(UserRole.OWNER, UserRole.ADMIN))
    """

    def __init__(self, *allowed_roles: UserRole):
        self.allowed_roles = allowed_roles

    def __call__(
        self,
        current_user: User = Depends(get_current_user)
    ) -> User:

        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied for role: {current_user.role}"
            )

        return current_user


# =====================================================
# FUNCTION-STYLE WRAPPER (FIXES IMPORT ERROR)
# =====================================================

def require_roles(*allowed_roles: UserRole) -> Callable:
    """
    Functional wrapper for RequireRoles.
    Keeps compatibility with:
        Depends(require_roles(...))
    """
    return RequireRoles(*allowed_roles)


# =====================================================
# ROLE GROUP HELPERS (BUSINESS-FRIENDLY)
# =====================================================

def AdminOnly():
    return RequireRoles(UserRole.ADMIN)


def RestaurantOwnerOnly():
    return RequireRoles(UserRole.OWNER)


def StaffOnly():
    return RequireRoles(UserRole.STAFF)


def InfluencerOnly():
    return RequireRoles(UserRole.INFLUENCER)


def OwnerOrStaff():
    return RequireRoles(UserRole.OWNER, UserRole.STAFF)


def AnyAuthenticatedUser():
    """
    Ensures user is logged in, regardless of role.
    """
    async def checker(
        current_user: User = Depends(get_current_user)
    ):
        return current_user

    return checker
