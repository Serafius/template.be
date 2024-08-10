import jwt
from config.mongodb import db
from bson import ObjectId
from datetime import datetime
from app.schemas.user_schema import userEntity
from app.internal.response_model import ResponseModel
from dotenv import load_dotenv
import os
from fastapi import Header, status
import traceback

load_dotenv()
ACCESS_TOKEN_SECRET = str(os.getenv("ACCESS_TOKEN_SECRET"))


def has_token(token: str = Header(title="token")):
    if not (token):
        return ResponseModel(data=None, isSuccess=False, error="Invalid Token", status= status.HTTP_400_BAD_REQUEST)
    try:
        payload = jwt.decode(token, ACCESS_TOKEN_SECRET, algorithms=["HS256"])
        #print("PAYLOAD", payload)
        dt = int(datetime.now().timestamp())
        if payload["expires"] < dt:
            return ResponseModel(data=None, isSuccess=False, error="Token Expired", status= status.HTTP_400_BAD_REQUEST)
        # if payload["nonce"]
        if payload["id"]:
            user = db.users.find_one({"_id": ObjectId(payload["id"])})
        else:
            return ResponseModel(data=None, isSuccess=False, error="Invalid ID", status= status.HTTP_400_BAD_REQUEST)
        if user:
            return userEntity(user)
        else:
            return ResponseModel(data=None, isSuccess=False, error="User Not Found", status= status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception has_token :", e)
        traceback.print_exc()
        return ResponseModel(data=None, isSuccess=False, error="Server Error", status= status.HTTP_500_INTERNAL_SERVER_ERROR)
