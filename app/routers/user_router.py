from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

# from config.mongodb import db
from ..schemas.user_schema import usersEntity
from ..internal.response_model import ResponseModel
from services.user.get_history import get_history as get_history_service
from fastapi import status
router = APIRouter()


@router.get("/all")
async def get_users(request: Request):
    db = request.app.state.db
    return ResponseModel(data=usersEntity(db.users.find()), isSuccess=True, error=None, status=status.HTTP_200_OK)


@router.get("/history")
async def get_history(response: ResponseModel = Depends(get_history_service)):
    return response
