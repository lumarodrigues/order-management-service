from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from oms.api import router
import os

app = FastAPI()

app.include_router(router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
