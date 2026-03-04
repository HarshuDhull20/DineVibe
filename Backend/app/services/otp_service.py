from datetime import datetime, timedelta, timezone
import hashlib
import random

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.otp import OTP, OTPChannel, OTPPurpose
from app.models.user import User
from app.services.email_service import send_email_otp
from app.services.sms_service import send_sms_otp


# =========================================================
# HASH OTP
# =========================================================
def _hash_otp(otp: str) -> str:
    return hashlib.sha256(otp.encode()).hexdigest()


# =========================================================
# GENERATE OTP
# =========================================================
async def generate_mfa_otp(db: AsyncSession, user: User, method: str):

    if method not in ["email", "sms"]:
        raise HTTPException(status_code=400, detail="Invalid OTP method")

    otp_code = str(random.randint(100000, 999999))
    hashed_otp = _hash_otp(otp_code)

    if method == "email":
        if not user.email:
            raise HTTPException(status_code=400, detail="Email not registered")

        destination = user.email
        channel = OTPChannel.EMAIL

        await send_email_otp(
            to_email=user.email,
            otp_code=otp_code,
            purpose="Login"
        )

    else:
        if not user.phone_number:
            raise HTTPException(status_code=400, detail="Phone not registered")

        destination = user.phone_number
        channel = OTPChannel.SMS

        # DEV MODE – print OTP in console
        print(f"📱 DEV SMS OTP for {user.phone_number}: {otp_code}")

        phone = user.phone_number
        if not phone.startswith("+"):
            phone = "+91" + phone  # assuming India
            send_sms_otp(
                phone_number=phone,
                otp_code=otp_code
            )

    otp = OTP(
        user_id=user.id,
        destination=destination,
        channel=channel,
        purpose=OTPPurpose.LOGIN,
        otp_hash=hashed_otp,
        is_verified=False,
        attempts=0,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=5)
    )

    db.add(otp)
    await db.commit()

    return otp_code  

# =========================================================
# VERIFY OTP
# =========================================================
async def verify_mfa_otp(db: AsyncSession, user: User, otp_code: str):

    hashed_input = _hash_otp(otp_code)

    result = await db.execute(
        select(OTP).where(
            OTP.user_id == user.id,
            OTP.otp_hash == hashed_input,
            OTP.is_verified == False
        )
    )

    otp = result.scalars().first()

    if not otp:
        raise HTTPException(status_code=401, detail="Invalid OTP")

    if otp.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="OTP expired")

    otp.is_verified = True
    await db.commit()

    return True