import asyncio
import app.models  

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import engine, AsyncSessionLocal, Base
from app.models.user import User, UserRole
from app.models.permission import Permission
from app.models.role_permission import RolePermission
from app.core.security import hash_password


# =========================================================
# PERMISSIONS
# =========================================================

PERMISSIONS = [
    "CREATE_RESERVATION",
    "VIEW_RESERVATION",
    "MANAGE_STAFF",
    "VIEW_ANALYTICS",
    "VIEW_AUDIT_LOGS",
    "UPDATE_SETTINGS",
]

ROLE_PERMISSION_MAPPING = {
    UserRole.ADMIN: PERMISSIONS,
    UserRole.RESTAURANT_OWNER: [
        "CREATE_RESERVATION",
        "VIEW_RESERVATION",
        "MANAGE_STAFF",
        "VIEW_ANALYTICS",
        "UPDATE_SETTINGS",
    ],
    UserRole.RESTAURANT_STAFF: [
        "CREATE_RESERVATION",
        "VIEW_RESERVATION",
    ],
    UserRole.NORMAL_USER: [],
    UserRole.SUPER_ADMIN: PERMISSIONS,  
}


# =========================================================
# SEED FUNCTION
# =========================================================

async def seed_database():
    print("🚀 Starting DineVibe database seeding...")

    # -----------------------------------------------------
    #  Create Tables 
    # -----------------------------------------------------
    async with engine.begin() as conn:
        print("📦 Creating tables (if not exist)...")
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:  

        # -------------------------------------------------
        #  Seed Permissions
        # -------------------------------------------------
        print("🔐 Seeding permissions...")

        for perm_code in PERMISSIONS:
            result = await db.execute(
                select(Permission).where(Permission.code == perm_code)
            )
            if not result.scalars().first():
                db.add(Permission(code=perm_code))

        await db.commit()

        # -------------------------------------------------
        #  Role → Permission Mapping
        # -------------------------------------------------
        print("🔗 Mapping roles to permissions...")

        for role, perm_list in ROLE_PERMISSION_MAPPING.items():
            for perm_code in perm_list:

                perm_result = await db.execute(
                    select(Permission).where(Permission.code == perm_code)
                )
                permission = perm_result.scalars().first()

                if not permission:
                    raise Exception(f"Permission {perm_code} not found")

                existing_mapping = await db.execute(
                    select(RolePermission).where(
                        RolePermission.role == role,
                        RolePermission.permission_id == permission.id
                    )
                )

                if not existing_mapping.scalars().first():
                    db.add(
                        RolePermission(
                            role=role,
                            permission_id=permission.id
                        )
                    )

        await db.commit()

        # -------------------------------------------------
        #  Create Super Admin (If Not Exists)
        # -------------------------------------------------
        print("👑 Checking for Super Admin...")
        admin_result = await db.execute(
            select(User).where(
                (User.role == UserRole.SUPER_ADMIN) |
                (User.email == "harshudhull12@gmail.com")
            )
        )
        existing_admin = admin_result.scalars().first()
        if not existing_admin:
            super_admin = User(
                username="super_admin",
                email="harshudhull12@gmail.com",
                phone_number="9949451580",  
                hashed_password=hash_password("SuperAdmin123"),
                role=UserRole.SUPER_ADMIN,
                is_active=True,
                is_mfa_enabled=True,
                must_change_password=True,
                is_first_login=True
            )
            db.add(super_admin)
            await db.commit()
            print("✅ Super Admin created")
            print("   Email: harshudhull12@gmail.com")
            print("   Password: SuperAdmin123")
        else:
            print("ℹ️ Super Admin already exists")

    print("🎯 Database seeding completed successfully.")


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    asyncio.run(seed_database())