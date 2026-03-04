import pytest
from httpx import AsyncClient

from app.main import app
from app.models.user import UserRole


# ---------------------------------------------------------
# HELPER: LOGIN AND GET TOKEN
# ---------------------------------------------------------

async def login_and_get_token(client, username, password):
    response = await client.post("/auth/login", json={
        "username": username,
        "password": password
    })
    assert response.status_code == 200
    return response.json()["access_token"]


# ---------------------------------------------------------
# NORMAL USER ACCESS TEST
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_normal_user_access_only_user_routes():
    """
    Feature:
    - Role-based login
    - Normal users cannot access admin/staff routes
    """

    async with AsyncClient(app=app, base_url="http://test") as ac:
        token = await login_and_get_token(ac, "normal_user", "User@123")
        headers = {"Authorization": f"Bearer {token}"}

        # Allowed
        me = await ac.get("/user/me", headers=headers)
        assert me.status_code == 200

        # Forbidden
        admin = await ac.get("/admin/audit-logs", headers=headers)
        assert admin.status_code == 403


# ---------------------------------------------------------
# RESTAURANT OWNER ACCESS TEST
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_owner_can_manage_restaurant_but_not_admin():
    """
    Feature:
    - Restaurant owner role
    - Cannot access super admin APIs
    """

    async with AsyncClient(app=app, base_url="http://test") as ac:
        token = await login_and_get_token(ac, "restaurant_owner", "Owner@123")
        headers = {"Authorization": f"Bearer {token}"}

        # Allowed
        profile = await ac.get("/user/me", headers=headers)
        assert profile.status_code == 200
        assert "manage_restaurant" in profile.json()["permissions"]

        # Forbidden
        admin = await ac.get("/admin/audit-logs", headers=headers)
        assert admin.status_code == 403


# ---------------------------------------------------------
# STAFF ACCESS ISOLATION
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_staff_cannot_access_owner_or_admin_routes():
    """
    Feature:
    - Staff login under restaurant
    - Staff session isolation
    """

    async with AsyncClient(app=app, base_url="http://test") as ac:
        token = await login_and_get_token(ac, "staff_user", "Staff@123")
        headers = {"Authorization": f"Bearer {token}"}

        # Allowed
        me = await ac.get("/user/me", headers=headers)
        assert me.status_code == 200
        assert "process_orders" in me.json()["permissions"]

        # Forbidden: Admin
        admin = await ac.get("/admin/audit-logs", headers=headers)
        assert admin.status_code == 403


# ---------------------------------------------------------
# INFLUENCER PERMISSION TEST
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_influencer_permissions():
    """
    Feature:
    - Permission-based API access
    """

    async with AsyncClient(app=app, base_url="http://test") as ac:
        token = await login_and_get_token(ac, "influencer_user", "Influencer@123")
        headers = {"Authorization": f"Bearer {token}"}

        me = await ac.get("/user/me", headers=headers)
        assert me.status_code == 200
        assert "create_campaigns" in me.json()["permissions"]

        # Influencer cannot access admin routes
        admin = await ac.get("/admin/audit-logs", headers=headers)
        assert admin.status_code == 403


# ---------------------------------------------------------
# SUPER ADMIN FULL ACCESS TEST
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_super_admin_full_access():
    """
    Feature:
    - Super admin role
    - Full system access
    """

    async with AsyncClient(app=app, base_url="http://test") as ac:
        token = await login_and_get_token(ac, "admin_dinevibe", "Admin@123")
        headers = {"Authorization": f"Bearer {token}"}

        # Admin APIs
        audit_logs = await ac.get("/admin/audit-logs", headers=headers)
        assert audit_logs.status_code == 200

        # User APIs
        me = await ac.get("/user/me", headers=headers)
        assert me.status_code == 200
        assert "all_access" in me.json()["permissions"]


# ---------------------------------------------------------
# TOKEN ROLE TAMPERING TEST
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_role_tampering_blocked():
    """
    Feature:
    - Security: JWT role tampering protection
    """

    fake_token = "Bearer invalid.jwt.token"

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/admin/audit-logs", headers={
            "Authorization": fake_token
        })

    assert response.status_code == 401
