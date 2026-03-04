from fastapi import Request
from typing import Dict
import hashlib


# --------------------------------------------------
# DEVICE PARSING UTILITIES
# --------------------------------------------------

def get_device_type(user_agent: str) -> str:
    """
    Determines device type based on User-Agent.
    """
    ua = user_agent.lower()

    if "mobile" in ua or "android" in ua or "iphone" in ua:
        return "mobile"
    if "tablet" in ua or "ipad" in ua:
        return "tablet"
    return "web"


def get_device_name(user_agent: str) -> str:
    """
    Extracts a human-readable device name.
    """
    ua = user_agent.lower()

    if "chrome" in ua:
        return "Chrome Browser"
    if "firefox" in ua:
        return "Firefox Browser"
    if "safari" in ua and "chrome" not in ua:
        return "Safari Browser"
    if "edge" in ua:
        return "Edge Browser"
    if "android" in ua:
        return "Android Device"
    if "iphone" in ua:
        return "iPhone"

    return "Unknown Device"


def get_client_ip(request: Request) -> str:
    """
    Extracts real client IP considering proxies / load balancers.
    """
    x_forwarded_for = request.headers.get("x-forwarded-for")

    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()

    return request.client.host if request.client else "unknown"


# --------------------------------------------------
# GEO LOCATION (BASIC / PLACEHOLDER)
# --------------------------------------------------

def get_geo_location(ip_address: str) -> str:
    """
    Placeholder for Geo-location.
    In production, integrate:
    - MaxMind
    - IPStack
    - Cloudflare
    """
    if ip_address.startswith("127.") or ip_address == "localhost":
        return "Localhost"

    return "Unknown Region"


# --------------------------------------------------
# DEVICE FINGERPRINTING
# --------------------------------------------------

def generate_device_fingerprint(
    user_agent: str,
    ip_address: str
) -> str:
    """
    Generates a stable fingerprint per device.
    Used for:
    - Trusted device logic
    - Skip MFA on known devices
    """
    raw = f"{user_agent}|{ip_address}"
    return hashlib.sha256(raw.encode()).hexdigest()


# --------------------------------------------------
# MASTER DEVICE INFO COLLECTOR
# --------------------------------------------------

def collect_device_info(request: Request) -> Dict:
    """
    Collects all device-related info in one place.
    Used during login/session creation.
    """
    user_agent = request.headers.get("user-agent", "unknown")

    ip_address = get_client_ip(request)

    return {
        "device_type": get_device_type(user_agent),
        "device_name": get_device_name(user_agent),
        "ip_address": ip_address,
        "location": get_geo_location(ip_address),
        "fingerprint": generate_device_fingerprint(user_agent, ip_address),
    }
