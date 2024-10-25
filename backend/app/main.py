# pylint: disable=W0621,W0613

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.health.health_controller import router as health_router
from app.db.mongodb import close_mongo_connection, connect_to_mongo
from app.api.endpoints import story
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(title=settings.project_name, lifespan=lifespan)

app.include_router(health_router, prefix="/api")
app.include_router(story.router, prefix="/api", tags=["stories"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
