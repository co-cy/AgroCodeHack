from fastapi.middleware.cors import CORSMiddleware
from app.config import UvicornConfig
from app import database, routes
from fastapi import FastAPI
from asyncio import run
import uvicorn

origins = [
    "*"
]

run(database.init_database())
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routes.init_routes(app)
uvicorn.run(app, **UvicornConfig())
