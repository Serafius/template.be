from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .routers import user_router, auth_router
import uvicorn
from .utils import Boto3Client
from dotenv import load_dotenv
import os
from .lifespan import app_lifespan

load_dotenv()
PORT = int(os.getenv("PORT", 5723))


app = FastAPI(lifespan=app_lifespan)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router, prefix="/users")
app.include_router(auth_router, prefix="/auth")


@app.get("/")
async def root():
    return "Server ready"

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
