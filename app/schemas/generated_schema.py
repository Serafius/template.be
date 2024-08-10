import json


def generatedVideoEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "uploadedId": item.get("uploadedId", ""),
        "owner": item.get("owner", ""),
        "link": item.get("link"),
        "language": item.get("language", ""),
        "createdDate": item.get("createdDate", ""),
        "updatedDate": item.get("updatedDate", ""),
        "success": item.get("success", False),
        "isDeleted": item.get("isDeleted", False),
        "timeTaken": item.get("timeTaken", 0),
        "thumbnail": item.get("thumbnail","https://media.stockimg.ai/image/_3CX05KC2Ge.png")
    }


def generatedVideosEntity(entity) -> list:
    return [generatedVideoEntity(item) for item in entity]
