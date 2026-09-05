from fastapi import APIRouter

from zettelkasten.api.routes import notes, ping

api_router = APIRouter()

api_router.include_router(notes.router)
api_router.include_router(ping.router)
