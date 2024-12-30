from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def setup_cors_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http//127.0.0.1:3000"],
        allow_credentials=True,
        allow_methods=["POST", "GET", "PUT"],
        allow_headers=["*"],
    )
