from fastapi import FastAPI

from . import index, get_map
from .user import registration, login, get_vineyards, set_vineyards


def init_routes(app: FastAPI):
    len_self_path = len(__name__.split("."))

    list_routes = [
        registration, index, login, get_map, get_vineyards, set_vineyards
    ]

    for route in list_routes:
        prefix = "/".join(route.__name__.split(".")[len_self_path:-1])
        if prefix:
            prefix = "/" + prefix
        app.include_router(route.router, prefix=prefix)
