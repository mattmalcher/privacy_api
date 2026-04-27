from contextlib import asynccontextmanager

from fastapi import FastAPI

from . import model
from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    model.load()
    yield


app = FastAPI(title="Privacy Filter API", lifespan=lifespan)
app.include_router(router)
