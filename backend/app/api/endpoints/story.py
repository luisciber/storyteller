from fastapi import APIRouter, HTTPException

from app.db.story_crud import (create_story, delete_story, get_stories,
                               get_story)
from app.models.story import Story
from app.story_generation.story_flow import UserPreferences, generate_story

router = APIRouter()


@router.post("/stories/", response_model=Story)
async def create_story_endpoint(
    user_preferences: UserPreferences
):
    story_data = await generate_story(user_preferences)
    story = Story(
        # Usando el primer título de capítulo como título de la historia
        title=story_data['outline'].chapter_titles[0],
        premise=story_data['outline'].premise,
        chapters=story_data['chapters']
    )
    return await create_story(story)


@router.get("/stories/", response_model=list[Story])
async def list_stories():
    return await get_stories()


@router.get("/stories/{story_id}", response_model=Story)
async def get_story_by_id(story_id: str):
    story = await get_story(story_id)
    if story is None:
        raise HTTPException(status_code=404, detail="Story not found")
    return story


@router.delete("/stories/{story_id}")
async def delete_story_by_id(story_id: str):
    delete_result = await delete_story(story_id)
    if delete_result == 0:
        raise HTTPException(status_code=404, detail="Story not found")
    return {"message": "Story deleted successfully"}
