from app.models.user_model import UserCreate
from app.schemas.user_schema import userEntity
import bcrypt

# from config.mongodb import db
import base64
from app.internal.response_model import ResponseModel
from app.dependencies.generate_token import generate_token
from fastapi import Request, status


async def login_user(request: Request, user: UserCreate):
    db = request.app.state.db
    #print("login_user", user)
    try:
        if not (user.email and user.password):
            return ResponseModel(
                data=None, isSuccess=False, error="email and password required", status=status.HTTP_400_BAD_REQUEST
            )
        email = user.email
        password = user.password
        user = db.users.find_one({"personalInfo.email": email})
        if user is not None:
            user = userEntity(user)
            if user["isVerified"] is True:
                control = bcrypt.checkpw(
                    password.encode("utf-8"),
                    base64.b64decode(user["auth"]["password"].encode("utf-8")),
                )
                if control:
                    token = generate_token(user["id"])
                    return ResponseModel(
                        data={
                            "user": {
                                "personalInfo": user["personalInfo"],
                                "plan": user["plan"],
                            },
                            "token": token["accessToken"],
                        },
                        isSuccess=True,
                        error=None,
                        status=status.HTTP_200_OK
                    )
                else:
                    return ResponseModel(
                        data=None, isSuccess=False, error="Wrong Password", status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return ResponseModel(
                    data=None, isSuccess=False, error="User Not Verified", status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return ResponseModel(
                data=None, isSuccess=False, error="User Not Found. Please Register", status=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
        print("Error login_user", e)
        return ResponseModel(data=None, isSuccess=False, error="Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
