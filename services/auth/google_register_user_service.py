from app.models.user_model import User, UserCreate
from app.schemas.user_schema import userEntity
from config.mongodb import db
from datetime import datetime, timedelta
from app.internal.response_model import ResponseModel
from app.dependencies.generate_token import generate_token
from fastapi import status

async def google_register_user(user: UserCreate):
    #print("register_user", user)
    try:
        name = user.name
        email = user.email
        pictureUrl = user.pictureUrl
        loginMethod = user.loginMethod
        id = user.id
        print("New User", email)

        dt = datetime.now()
        newUser: User = {
            "personalInfo": {
                "name": name,
                "email": email,
                "pictureUrl": pictureUrl,
                "about": "",
                "credits": 0,
            },
            "credentials": {"loginMethod": loginMethod, "ids": [id]},
            "plan": {
                "id": "free-plan",
                "name": "free",
                "credits": 0,
            },
            "auth": {"password": None},
            "customerIds": [],
            "isDeleted": False,
            "isVerified": False,
            "createdDate": dt,
            "updatedDate": dt,
        }
        #print("new", newUser)
        db.users.insert_one(newUser)
        
        user = userEntity(db.users.find_one({"personalInfo.email": email}))
        token = generate_token(user["id"])
        return ResponseModel(
            data={
                "user": {
                    "personalInfo": user["personalInfo"],
                    "plan": user["plan"],
                },
                "token": token["accessToken"]
            },
            isSuccess=True,
            error=None,
            status= status.HTTP_200_OK
        )
    except Exception as e:
        print("Error google_register_user", e)
        return ResponseModel(data= None, isSuccess=True, error="Error", status= status.HTTP_500_INTERNAL_SERVER_ERROR)    

    # accessToken = jwt.encode(
    #         {
    #             "id": id,
    #             "expires": int(
    #                 (datetime.now() + timedelta(days=1)).timestamp()
    #             ),
    #             "nonce": "nonce",
    #         },
    #         "24d208ba60909f9a930dcddfb05302f57a3eaba879d599ac42c9d1d38b",
    #         algorithm="HS256",
    #     )
    # refreshToken = jwt.encode(
    #     {
    #         "id": id,
    #         "nonce": "nonce",
    #     },
    #     "dbc426ef673223481b67960d5041ae92c3a6b0d6fa0b29b159e0d1246",
    #     algorithm="HS256",
    # )
    # token = {"accessToken" : accessToken, "refreshToken": refreshToken}
    # return token