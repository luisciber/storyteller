# pylint: disable=W0621,W0613

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.health.health_controller import router as health_router
from app.db.mongodb import close_mongo_connection, connect_to_mongo


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(title="StoryTeller API", lifespan=lifespan)

app.include_router(health_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
