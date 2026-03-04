from twilio.rest import Client
from app.config.settings import settings


def send_sms_otp(phone_number: str, otp_code: str):
    client = Client(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN
    )

    message = client.messages.create(
        body=f"Your DineVibe OTP is {otp_code}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )

    return message.sid