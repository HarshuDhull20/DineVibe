from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.permission import Permission
from app.models.role_permission import RolePermission


def require_permission(permission_code: str):
    """
    Dynamic permission dependency.
    Usage:
        Depends(require_permission("CREATE_RESERVATION"))
    """

    async def permission_dependency(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):

        # Get permission
        result = await db.execute(
            select(Permission).where(Permission.code == permission_code)
        )
        permission = result.scalars().first()

        if not permission:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Permission not configured in database"
            )

        # Check role-permission mapping
        result = await db.execute(
            select(RolePermission).where(
                RolePermission.role == current_user.role,
                RolePermission.permission_id == permission.id
            )
        )
        mapping = result.scalars().first()

        if not mapping:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action"
            )

        return current_user

    return permission_dependency
