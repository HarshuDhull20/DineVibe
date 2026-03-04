import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.database.db import get_db
from app.models.user import UserRole
from app.config.settings import settings

# ---------------------------------------------------------
# TEST CONFIG
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"


# ---------------------------------------------------------
# REGISTRATION TESTS
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_register_normal_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/register", json={
            "username": "normal_user_1",
            "email": "normal1@test.com",
            "phone_number": "+919999999001",
            "password": "StrongPass@123",
            "role": UserRole.NORMAL
        })

    assert response.status_code == 201
    assert response.json()["role"] == UserRole.NORMAL


@pytest.mark.asyncio
async def test_duplicate_registration_fails():
    payload = {
        "username": "dup_user",
        "email": "dup@test.com",
        "phone_number": "+919999999002",
        "password": "StrongPass@123",
        "role": UserRole.NORMAL
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/register", json=payload)
        response = await ac.post("/auth/register", json=payload)

    assert response.status_code == 400
    assert "exists" in response.json()["detail"].lower()


# ---------------------------------------------------------
# PASSWORD LOGIN (NORMAL USER)
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_password_login_success():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/auth/login",
            data={
                "username": "normal_user_1",
                "password": "StrongPass@123"
            }
        )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


# ---------------------------------------------------------
# OTP LOGIN (RESTAURANT OWNER)
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_otp_login_invalid():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/login/otp", json={
            "phone_number": "+919999999999",
            "otp_code": "000000"
        })

    assert response.status_code == 401


# ---------------------------------------------------------
# ACCOUNT LOCK AFTER FAILED ATTEMPTS
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_account_lock_after_multiple_failures():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        for _ in range(settings.MAX_LOGIN_ATTEMPTS):
            await ac.post(
                "/auth/login",
                data={
                    "username": "normal_user_1",
                    "password": "WRONG_PASSWORD"
                }
            )

        
        response = await ac.post(
            "/auth/login",
            data={
                "username": "normal_user_1",
                "password": "StrongPass@123"
            }
        )

    assert response.status_code == 403
    assert "locked" in response.json()["detail"].lower()


# ---------------------------------------------------------
# AUTHORIZATION TEST 
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_me_endpoint_authorized():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        login = await ac.post(
            "/auth/login",
            data={
                "username": "admin_dinevibe",
                "password": "Admin@123"
            }
        )

        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = await ac.get("/user/me", headers=headers)

    assert response.status_code == 200
    assert "permissions" in response.json()
    assert "manage_users" in response.json()["permissions"]


# ---------------------------------------------------------
# GLOBAL LOGOUT TEST
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_global_logout():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        login = await ac.post(
            "/auth/login",
            data={
                "username": "admin_dinevibe",
                "password": "Admin@123"
            }
        )

        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = await ac.post("/auth/logout", headers=headers)
        assert response.status_code == 200

        # Token should now be invalid
        me = await ac.get("/user/me", headers=headers)
        assert me.status_code in (401, 403)
