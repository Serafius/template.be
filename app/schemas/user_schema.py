import json
def userEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "personalInfo": json.loads(json.dumps(item["personalInfo"])),
        "credentials": json.loads(json.dumps(item["credentials"])),
        "plan": json.loads(json.dumps(item["plan"])),
        "auth": json.loads(json.dumps(item["auth"])),
        "customerIds": json.loads(json.dumps(item["customerIds"])),
        "isDeleted": item.get("isDeleted",False),
        "isVerified": item.get("isVerified",True),
        "createdDate": item["createdDate"],
        "updatedDate": item["updatedDate"]
    }
    
def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]    