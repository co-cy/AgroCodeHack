from fastapi.middleware.cors import CORSMiddleware
from app.config import UvicornConfig
from app import database, routes
from fastapi import FastAPI
import uvicorn


origins = [
    "*"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routes.init_routes(app)


@app.on_event("startup")
async def startup_event():
    await database.init_database()

uvicorn.run(app, **UvicornConfig())

