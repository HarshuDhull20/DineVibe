import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status
from dotenv import load_dotenv

load_dotenv()

# =====================================================
# CONFIGURATION
# =====================================================

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set in environment")

ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
REFRESH_TOKEN_EXPIRE_DAYS = 30

OTP_EXPIRY_SECONDS = 300
MAX_LOGIN_ATTEMPTS = 5

# =====================================================
# PASSWORD HASHING (bcrypt via passlib)
# =====================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    """
    Hash plaintext password safely.
    """

    #  Prevent double hashing
    if password.startswith("$2a$") or password.startswith("$2b$"):
        raise RuntimeError("DOUBLE HASH DETECTED")

    #  bcrypt-safe truncation (industry standard)
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]

    return pwd_context.hash(password_bytes.decode("utf-8", errors="ignore"))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against stored hash.
    """
    return pwd_context.verify(plain_password, hashed_password)

# =====================================================
# JWT TOKEN CREATION
# =====================================================

def create_access_token(
    user_id: int,
    role: str,
    expires_delta: Optional[timedelta] = None
):
    """
    Create JWT access token WITH JTI
    Returns: token, jti, expire
    """

    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    jti = secrets.token_urlsafe(32)

    payload = {
        "sub": str(user_id),
        "role": role,
        "jti": jti,
        "iat": now,
        "exp": expire,
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token, jti, expire



def create_refresh_token() -> str:
    """
    Generate secure refresh token.
    """
    return secrets.token_urlsafe(64)


def decode_token(token: str) -> dict:
    """
    Decode and validate JWT token.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# =====================================================
# OTP GENERATION & VALIDATION
# =====================================================

def generate_otp() -> str:
    return str(secrets.randbelow(900000) + 100000)


def is_otp_expired(created_at: datetime) -> bool:
    return datetime.now(timezone.utc) > created_at + timedelta(seconds=OTP_EXPIRY_SECONDS)

# =====================================================
# LOGIN ATTEMPT PROTECTION
# =====================================================

def check_account_lock(user):
    if user.failed_login_attempts >= MAX_LOGIN_ATTEMPTS:
        user.is_active = False
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account locked due to multiple failed login attempts"
        )


def record_failed_login(user):
    user.failed_login_attempts += 1


def reset_failed_login(user):
    user.failed_login_attempts = 0
    user.last_login_at = datetime.now(timezone.utc)

# =====================================================
# MFA HELPERS
# =====================================================

def generate_totp_secret() -> str:
    return secrets.token_hex(20)
