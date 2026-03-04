import time
from typing import Dict, Tuple

# --------------------------------------------------
# CONFIGURATION (MATCHES YOUR FEATURE LIST)
# --------------------------------------------------

LOGIN_ATTEMPT_LIMIT = 5          # Max attempts
LOGIN_WINDOW_SECONDS = 300       # 5 minutes

OTP_REQUEST_LIMIT = 3            # OTP sends
OTP_WINDOW_SECONDS = 300         # 5 minutes

API_REQUEST_LIMIT = 100          # Per session
API_WINDOW_SECONDS = 60          # Per minute


# --------------------------------------------------
# IN-MEMORY STORE (REPLACE WITH REDIS IN PROD)
# --------------------------------------------------

_login_attempts: Dict[str, Tuple[int, float]] = {}
_otp_attempts: Dict[str, Tuple[int, float]] = {}
_api_requests: Dict[str, Tuple[int, float]] = {}


# --------------------------------------------------
# GENERIC RATE LIMIT CHECKER
# --------------------------------------------------

def _check_limit(
    store: Dict[str, Tuple[int, float]],
    key: str,
    limit: int,
    window_seconds: int
) -> bool:
    """
    Returns True if allowed, False if rate-limited.
    """
    now = time.time()

    if key not in store:
        store[key] = (1, now)
        return True

    count, first_timestamp = store[key]

    if now - first_timestamp > window_seconds:
        store[key] = (1, now)
        return True

    if count >= limit:
        return False

    store[key] = (count + 1, first_timestamp)
    return True


# --------------------------------------------------
# LOGIN RATE LIMITING
# --------------------------------------------------

def check_login_rate_limit(identifier: str) -> bool:
    """
    Identifier = email OR phone OR IP.
    """
    return _check_limit(
        store=_login_attempts,
        key=f"login:{identifier}",
        limit=LOGIN_ATTEMPT_LIMIT,
        window_seconds=LOGIN_WINDOW_SECONDS
    )


# --------------------------------------------------
# OTP RATE LIMITING
# --------------------------------------------------

def check_otp_rate_limit(phone_or_email: str) -> bool:
    """
    Prevent OTP spam.
    """
    return _check_limit(
        store=_otp_attempts,
        key=f"otp:{phone_or_email}",
        limit=OTP_REQUEST_LIMIT,
        window_seconds=OTP_WINDOW_SECONDS
    )


# --------------------------------------------------
# API RATE LIMITING (PER SESSION)
# --------------------------------------------------

def check_api_rate_limit(session_id: str) -> bool:
    """
    Per-session API protection.
    """
    return _check_limit(
        store=_api_requests,
        key=f"api:{session_id}",
        limit=API_REQUEST_LIMIT,
        window_seconds=API_WINDOW_SECONDS
    )


# --------------------------------------------------
# RESET HELPERS
# --------------------------------------------------

def reset_login_attempts(identifier: str):
    _login_attempts.pop(f"login:{identifier}", None)


def reset_otp_attempts(phone_or_email: str):
    _otp_attempts.pop(f"otp:{phone_or_email}", None)


def reset_api_limits(session_id: str):
    _api_requests.pop(f"api:{session_id}", None)
