from fastapi import FastAPI

from . import index


def init_routes(app: FastAPI):
    app.include_router(index.router)
