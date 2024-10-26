from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.models.story import Story

client = AsyncIOMotorClient(settings.mongodb_url)
db = client[settings.database_name]
story_collection = db["stories"]


async def create_story(story: Story):
    story_dict = story.model_dump(by_alias=True, exclude={"id"})
    new_story = await story_collection.insert_one(story_dict)
    created_story = await story_collection.find_one({"_id": new_story.inserted_id})
    return Story(**{**created_story, "id": str(created_story["_id"])})


async def get_stories():
    stories = []
    async for story in story_collection.find({}, {"chapters": 0}):
        stories.append(
            Story(**{**story, "id": str(story["_id"]), "chapters": []})
        )
    return stories


async def get_story(story_id: str):
    story = await story_collection.find_one({"_id": ObjectId(story_id)})
    if story:
        return Story(**{**story, "id": str(story["_id"])})


async def delete_story(story_id: str):
    delete_result = await story_collection.delete_one({"_id": ObjectId(story_id)})
    return delete_result.deleted_count
