from fastapi import Depends, status
from app.models.user_model import UserCheck
from app.dependencies import check_user_exists
from app.internal.response_model import ResponseModel
from services.auth.google_register_user_service import (
    google_register_user as google_register_user_service,
)
from services.auth.google_login_user_service import (
    google_login_user as google_login_user_service,
)


async def google_user(user: UserCheck, user_exists=Depends(check_user_exists)):
    #print("check_user", user)
    try:
        if not user_exists:
            response = await google_register_user_service(user)
            return response
        else:
            response = await google_login_user_service(user)
            return response

    except Exception as e:
        print("Exception google_user :", e)
        return ResponseModel(data=None, isSuccess=False, error="Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
