# DELETE THIS FILE IF NO ERROR OCCURS

from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
URI = os.getenv("MONGODB_URI")
client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017/"))

db = client["template"]

try:
    client.admin.command("ping")
except Exception as e:
    print(e)
