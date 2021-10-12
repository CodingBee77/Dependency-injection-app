from fastapi import FastAPI
from app.app_container import Application
from fastapi.middleware.cors import CORSMiddleware
import app.endpoints as endpoints
from app import models
from sqlalchemy import create_engine


def create_app() -> FastAPI:
    container = Application()
    # container.config.from_yaml("config.yml")
    container.wire(modules=[endpoints])

    # db = container.databases.db_provider.provided
    # db.create_database()
    engine = create_engine("sqlite:///./app.db", echo=True)
    models.Base.metadata.create_all(bind=engine)
    app = FastAPI()
    app.container = container
    app.include_router(endpoints.router)
    return app


app = create_app()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)