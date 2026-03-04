import httpx
from typing import Dict, Any
from app.config.settings import settings


class HTTPClient:
    """
    Centralized async HTTP client
    Used for OTP, Email, SMS, OAuth providers
    """

    def __init__(self):
        self.timeout = 10.0

    async def post(
        self,
        url: str,
        payload: Dict[str, Any],
        headers: Dict[str, str] | None = None,
    ):
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                url,
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            return response.json()

    async def get(
        self,
        url: str,
        headers: Dict[str, str] | None = None,
    ):
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()


http_client = HTTPClient()
