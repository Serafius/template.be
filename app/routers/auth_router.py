from fastapi import Depends, APIRouter
from ..internal.response_model import ResponseModel
from services.auth.google_user_service import google_user as google_user_service
from services.auth.login_user_service import login_user as login_user_service
from services.auth.register_user_service import register_user as register_user_service
from services.auth.verify_user_service import verify_user as verify_user_service

router = APIRouter()

@router.post("/user")
async def google_user(response: ResponseModel = Depends(google_user_service)):
    return response

@router.post("/register")
async def register_user(response: ResponseModel = Depends(register_user_service)):
    return response

@router.post("/login")
async def login_user(response: ResponseModel = Depends(login_user_service)):
    return response

@router.post("/verify")
async def verify_user(response: ResponseModel = Depends(verify_user_service)):
    return response