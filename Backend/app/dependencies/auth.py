from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import JWTError

from app.database.db import get_db
from app.models.user import User, UserRole
from app.models.session import UserSession
from app.models.permission import Permission
from app.models.role_permission import RolePermission
from app.core.security import decode_token

# =====================================================
# OAuth2
# =====================================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/password")

# =====================================================
# GET CURRENT USER WITH SESSION VALIDATION
# =====================================================

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)

        user_id = payload.get("sub")
        jti = payload.get("jti")

        if user_id is None or jti is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    #  Validate active session
    result = await db.execute(
        select(UserSession).where(
            UserSession.access_token_jti == jti,
            UserSession.is_active == True
        )
    )
    session = result.scalars().first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session revoked or expired"
        )

    #  Fetch user
    result = await db.execute(
        select(User).where(User.id == int(user_id))
    )
    user = result.scalars().first()

    if not user:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated"
        )

    return user

# =====================================================
# ROLE CHECKER (RBAC)
# =====================================================

class RoleChecker:
    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        return user

# =====================================================
# PERMISSION CHECKER (DB-BASED)
# =====================================================

def PermissionChecker(required_permission: str):

    async def checker(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):

        result = await db.execute(
            select(RolePermission)
            .join(Permission)
            .where(
                RolePermission.role == user.role,
                Permission.code == required_permission
            )
        )

        permission = result.scalars().first()

        if not permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )

        return True

    return checker
