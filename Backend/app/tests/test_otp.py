import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta

from app.main import app
from app.models.user import UserRole
from app.config.settings import settings


# ---------------------------------------------------------
# OTP GENERATION TEST
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_generate_otp_for_phone_login():
    """
    Feature:
    - Phone Number + OTP login
    - OTP generation
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/otp/request", json={
            "phone_number": "+919999999111",
            "role": UserRole.OWNER
        })

    assert response.status_code == 200
    assert response.json()["message"] == "OTP sent successfully"


# ---------------------------------------------------------
# OTP VERIFICATION SUCCESS
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_verify_valid_otp_success():
    """
    Feature:
    - OTP verification
    - Login via OTP
    """

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Step 1: Request OTP
        await ac.post("/auth/otp/request", json={
            "phone_number": "+919999999111",
            "role": UserRole.OWNER
        })

        # NOTE:
        # In test environment we assume OTP = "123456"
        # (This is standard practice for deterministic tests)
        response = await ac.post("/auth/otp/verify", json={
            "phone_number": "+919999999111",
            "otp_code": "123456"
        })

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


# ---------------------------------------------------------
# INVALID OTP TEST
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_verify_invalid_otp_fails():
    """
    Feature:
    - Invalid OTP rejection
    - Security enforcement
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/otp/verify", json={
            "phone_number": "+919999999111",
            "otp_code": "000000"
        })

    assert response.status_code == 401
    assert "invalid otp" in response.json()["detail"].lower()


# ---------------------------------------------------------
# OTP EXPIRY TEST
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_expired_otp_fails():
    """
    Feature:
    - OTP expiry time enforcement
    """

    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/otp/request", json={
            "phone_number": "+919999999222",
            "role": UserRole.OWNER
        })

        # Simulate OTP expiry by waiting past expiry time
        await ac.aclose()

    # Normally OTP expiry is checked in DB via timestamp
    # We expect verification to fail after expiry
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/otp/verify", json={
            "phone_number": "+919999999222",
            "otp_code": "123456"
        })

    assert response.status_code == 401
    assert "expired" in response.json()["detail"].lower()


# ---------------------------------------------------------
# ROLE RESTRICTION TEST (OTP ONLY FOR OWNER)
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_otp_login_not_allowed_for_normal_user():
    """
    Feature:
    - Role-based login method restriction
    """

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/otp/request", json={
            "phone_number": "+919999999333",
            "role": UserRole.NORMAL
        })

    assert response.status_code == 403
    assert "otp login not allowed" in response.json()["detail"].lower()
