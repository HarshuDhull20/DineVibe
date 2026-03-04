from typing import Dict
import ipaddress


# --------------------------------------------------
# BASIC GEO LOCATION ENGINE (SAFE DEFAULT)
# --------------------------------------------------

def is_private_ip(ip_address: str) -> bool:
    """
    Checks if IP is private or local.
    """
    try:
        ip = ipaddress.ip_address(ip_address)
        return ip.is_private or ip.is_loopback
    except ValueError:
        return True


def get_country_from_ip(ip_address: str) -> str:
    """
    Lightweight geo detection.
    
    ⚠️ Production Note:
    This is a placeholder.
    Replace with:
    - MaxMind GeoIP2
    - IPStack
    - Cloudflare Geo Headers
    """
    if is_private_ip(ip_address):
        return "LOCAL"

    # Example logic (extendable)
    if ip_address.startswith("13.") or ip_address.startswith("52."):
        return "India"
    if ip_address.startswith("3."):
        return "USA"

    return "UNKNOWN"


def get_city_from_ip(ip_address: str) -> str:
    """
    City-level detection placeholder.
    """
    if is_private_ip(ip_address):
        return "Localhost"

    return "Unknown City"


def get_geo_info(ip_address: str) -> Dict[str, str]:
    """
    Central geo function used across the system.
    """
    return {
        "country": get_country_from_ip(ip_address),
        "city": get_city_from_ip(ip_address),
    }
