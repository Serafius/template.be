from app.models.user_model import UserCreate
from app.schemas.user_schema import userEntity
from config.mongodb import db
from app.internal.response_model import ResponseModel
from app.dependencies.generate_token import generate_token
from fastapi import status

async def google_login_user(user: UserCreate):
    #print("login_user", user)
    try:
        email = user.email
        name = user.name
        pictureUrl = user.pictureUrl
        user = userEntity(db.users.find_one_and_update({"personalInfo.email": email}, 
            {"$set": {"personalInfo.name": name, "personalInfo.pictureUrl": pictureUrl}}, return_document=True))
        token = generate_token(user["id"])
        return ResponseModel(
            data={
                "user": user,
                "token": token["accessToken"]
            },
            isSuccess=True,
            error=None,
            status= status.HTTP_200_OK
        )
    except Exception as e:
        print("Error google_login_user", e)
        return ResponseModel(data= None, isSuccess=True, error="Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
