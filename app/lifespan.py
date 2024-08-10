# lifespan.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .utils import Boto3Client
from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient

load_dotenv()

PORT = int(os.getenv("PORT", 5723))

URI = os.getenv("MONGODB_URI") or "mongodb://localhost:27017/template"


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # Load resources on startup
    print(f"Server is starting on port {PORT}")
    client = MongoClient(URI)
    db = client["template"]
    app.state.client = client
    app.state.db = db
    print("mongodb connected")
    app.state.boto3 = Boto3Client.get_client()
    print("boto3 connected")

    yield

    # Cleanup resources on shutdown
    print("Shutting down")
    app.state.client.close()
