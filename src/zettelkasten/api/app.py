from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from zettelkasten.api.config import allowed_origins
from zettelkasten.api.routes.api import api_router

app = FastAPI(
    title="AI Zettelkasten API",
    version="0.1.0",
)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
