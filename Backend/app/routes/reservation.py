from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.base import get_db
from app.dependencies.permission import require_permission
from app.models.user import User

router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"]
)


# -----------------------------------------------------
# CREATE RESERVATION
# -----------------------------------------------------
@router.post("/")
async def create_reservation(
    user: User = Depends(require_permission("CREATE_RESERVATION")),
):
    return {
        "message": "Reservation created successfully",
        "created_by": user.username
    }


# -----------------------------------------------------
# VIEW RESERVATIONS
# -----------------------------------------------------
@router.get("/")
async def list_reservations(
    user: User = Depends(require_permission("VIEW_RESERVATION")),
):
    return {
        "message": "Reservations list",
        "requested_by": user.username
    }
