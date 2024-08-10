from fastapi import HTTPException, Depends, Request
from ..models.user_model import UserCheck

# from config.mongodb import db


def get_user_collection(request: Request):
    db = request.app.state.db
    return db


async def check_user_exists(user: UserCheck, collection=Depends(get_user_collection)):
    return (
        collection.users.count_documents(
            {"personalInfo.email": user.email, "isDeleted": False}
        )
        > 0
    )
