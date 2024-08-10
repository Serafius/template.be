from fastapi import Depends, Request, status

from middlewares.has_token import has_token
from app.internal.response_model import ResponseModel
from app.schemas.generated_schema import generatedVideosEntity


async def get_history(
    request: Request, page: int = 1, count: int = 10, user: dict = Depends(has_token)
):
    page = page - 1
    db = request.app.state.db
    
    try:
        if user.get('data', 0) == None:
            return ResponseModel(data=None, isSuccess=False, error=user.get('error', "Error"), status= user.get('status',status.HTTP_500_INTERNAL_SERVER_ERROR))
        
        videos = generatedVideosEntity(
            db.generated.find({"owner": user["id"], "success": True, 
            "$or": [{"isDeleted": {"$exists": False}}, {"isDeleted": False}]})
            .sort([("createdDate", -1)])
            .skip(page * count)
            .limit(count)
        )
        
        if len(videos) - (page * count) <= count:
            isLastPage = True
        else:
            isLastPage = False
            
        return ResponseModel(
            data={"videos": videos, "isLastPage": isLastPage},
            isSuccess=True,
            error=None,
            status= status.HTTP_200_OK
        )
    except Exception as e:
        print("Error get_history", e)
        return ResponseModel(data=None, isSuccess=False, error="Error", status= status.HTTP_500_INTERNAL_SERVER_ERROR)
