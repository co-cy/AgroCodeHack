from app import database, routes
from fastapi import FastAPI
from asyncio import run
import uvicorn


run(database.init_database())
app = FastAPI()

routes.init_routes(app)
uvicorn.run(app)
