from app.schemas.user_schema import userEntity
from fastapi import Request, status

# from config.mongodb import db
from datetime import datetime
import jwt
from bson import ObjectId
from app.internal.response_model import ResponseModel
from app.dependencies.generate_token import generate_token
from dotenv import load_dotenv
import os

load_dotenv()
VERIFY_TOKEN_SECRET = str(os.getenv("VERIFY_TOKEN_SECRET"))


async def verify_user(request: Request, token: str, code: str):
    db = request.app.state.db
    if not (token and code):
        return ResponseModel(
            data=None, isSuccess=False, error="token and code required", status=status.HTTP_400_BAD_REQUEST
        )
    try:
        payload = jwt.decode(
            token,
            VERIFY_TOKEN_SECRET,
            algorithms=["HS256"],
        )
        if payload["verifyCode"] == code:
            dt = int(datetime.now().timestamp())
            #print(dt, payload["expires"])
            if payload["expires"] > dt:
                user = userEntity(
                    db.users.find_one_and_update(
                        {"_id": ObjectId(payload["id"])},
                        {"$set": {"isVerified": True}},
                        return_document=True,
                    )
                )
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
                return ResponseModel(data=None, isSuccess=False, error="Token Expired", status=status.HTTP_400_BAD_REQUEST)
        else:
            return ResponseModel(data=None, isSuccess=False, error="Wrong Verify Code", status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Error verify_user", e)
        return ResponseModel(data=None, isSuccess=False, error="Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
