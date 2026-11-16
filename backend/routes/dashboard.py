from fastapi import APIRouter, Depends

from auth import get_current_user
from models.user import User
from services.dashboard_service import get_dashboard_summary

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("")
def dashboard(current_user: User = Depends(get_current_user)):
    return get_dashboard_summary(current_user.id)
