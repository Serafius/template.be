from app.models.user_model import User, UserCreate
from app.schemas.user_schema import userEntity

# from config.mongodb import db
from random import randint
from datetime import datetime, timedelta
import bcrypt
import base64
import jwt
from app.internal.response_model import ResponseModel
from app.dependencies.send_verification_mail import send_verification_mail
from fastapi import Request, status


async def register_user(request: Request, user: UserCreate):
    #print("register_user", user)
    db = request.app.state.db
    # blog_data = blog.dict()
    # blog_data["created_at"] = datetime.utcnow()
    # blog_data["updated_at"] = datetime.utcnow()

    # result = await collection.insert_one(blog_data)
    try:
        if not (user.email and user.password):
            return ResponseModel(
                data=None, isSuccess=False, error="email and password required", status=status.HTTP_400_BAD_REQUEST
            )
        if user.name is not None:
            name = user.name
        else:
            name = "user" + str(randint(100000, 999999))

        email = user.email
        password = user.password
        #print(name, email, password)

        if (
            db.users.count_documents({"personalInfo.email": email, "isDeleted": False})
            == 1
        ):
            return ResponseModel(
                data=None, isSuccess=False, error="User Already Exist. Please Login", status=status.HTTP_400_BAD_REQUEST
            )

        salt = bcrypt.gensalt()
        hashed_password_b = bcrypt.hashpw(password.encode("utf-8"), salt)
        hashed_password = base64.b64encode(hashed_password_b).decode("utf-8")

        #print("password", hashed_password)
        # print(
        #     "control",
        #     bcrypt.checkpw(
        #         password.encode("utf-8"),
        #         base64.b64decode(hashed_password.encode("utf-8")),
        #     ),
        # )

        if (
            db.users.count_documents({"personalInfo.email": email, "isDeleted": True})
            == 1
        ):
            #print("return")
            user = userEntity(db.users.find_one({"personalInfo.email": email}))
            dt = datetime.now()
            db.users.find_one_and_update(
                {"personalInfo.email": email},
                {
                    "$set": {
                        "personalInfo.credits": 0,
                        "plan": {"id": "free-plan", "name": "free", "credits": 0},
                        "auth.password": hashed_password,
                        "isDeleted": False,
                        "updatedDate": dt,
                    }
                },
            )

        else:
            #print("new")
            dt = datetime.now()
            newUser: User = {
                "personalInfo": {
                    "name": name,
                    "email": email,
                    "pictureUrl": "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png",
                    "about": "",
                    "credits": 0,
                },
                "credentials": {"loginMethod": "email"},
                "plan": {
                    "id": "free-plan",
                    "name": "free",
                    "credits": 0,
                },
                "auth": {"password": hashed_password},
                "customerIds": [],
                "isDeleted": False,
                "isVerified": False,
                "createdDate": dt,
                "updatedDate": dt,
            }
            #print(newUser)
            db.users.insert_one(newUser)

        user = userEntity(db.users.find_one({"personalInfo.email": email}))

        verify_code = str(randint(1000, 9999))
        expires = int((datetime.now() + timedelta(days=1)).timestamp())
        payload = {
            "id": user["id"],
            "expires": expires,
            "nonce": "nonce",
            "verifyCode": verify_code,
        }
        token = jwt.encode(
            payload,
            "9ac42c9d1d38b9f8a553e5b4bcfa80b19003f3d614edfa0cb8456afcce",
            algorithm="HS256",
        )

        # token_db[email] = (token, expires)

        send_verification_mail(user["personalInfo"]["name"], verify_code)

        return ResponseModel(
            data={"verifyToken": token, "expires": expires}, isSuccess=True, error=None, status=status.HTTP_200_OK
        )
    except Exception as e:
        print("Error register_user", e)
        return ResponseModel(data=None, isSuccess=False, error="Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
