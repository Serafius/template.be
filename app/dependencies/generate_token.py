from datetime import datetime, timedelta
import jwt
from dotenv import load_dotenv
import os

load_dotenv()
ACCESS_TOKEN_SECRET = str(os.getenv("ACCESS_TOKEN_SECRET"))
REFRESH_TOKEN_SECRET = str(os.getenv("REFRESH_TOKEN_SECRET"))

def generate_token(id):
    accessToken = jwt.encode(
            {
                "id": id,
                "expires": int(
                    (datetime.now() + timedelta(days=1)).timestamp()
                ),
                "nonce": "nonce",
            },
            ACCESS_TOKEN_SECRET,
            algorithm="HS256",
        )
    refreshToken = jwt.encode(
        {
            "id": id,
            "nonce": "nonce",
        },
        REFRESH_TOKEN_SECRET,
        algorithm="HS256",
    )
    token = {"accessToken": accessToken, "refreshToken": refreshToken}
    return token