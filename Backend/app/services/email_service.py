import requests
from fastapi import HTTPException
from app.config.settings import settings


async def send_email_otp(to_email: str, otp_code: str, purpose: str):
    """
    Sends OTP email using Brevo (Sendinblue).
    """

    if not settings.BREVO_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="BREVO_API_KEY missing in environment"
        )

    if not settings.SENDER_EMAIL:
        raise HTTPException(
            status_code=500,
            detail="SENDER_EMAIL missing in environment"
        )

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json"
    }

    data = {
        "sender": {
            "email": settings.SENDER_EMAIL,
            "name": "DineVibe"
        },
        "to": [
            {
                "email": to_email
            }
        ],
        "subject": f"DineVibe {purpose} OTP",
        "htmlContent": f"""
            <div style="font-family: Arial, sans-serif;">
                <h2>DineVibe Verification</h2>
                <p>Your OTP Code is:</p>
                <h1 style="color:#2563eb;">{otp_code}</h1>
                <p>This code expires in {settings.OTP_EXPIRY_SECONDS // 60} minutes.</p>
                <p>If you did not request this, ignore this email.</p>
            </div>
        """
    }

    try:
        response = requests.post(url, json=data, headers=headers)

        print("Brevo Status Code:", response.status_code)
        print("Brevo Response:", response.text)

        if response.status_code != 201:
            raise Exception(response.text)

        print("✅ OTP Email sent via Brevo")

    except Exception as e:
        print("❌ Brevo Email Error:", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Email sending failed: {str(e)}"
        )