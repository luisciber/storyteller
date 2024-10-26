from app.models.base import Model
from app.story_generation.story_flow import Chapter, UserPreferences


class Story(Model):
    title: str
    image_url: str
    premise: str
    chapters: list[Chapter]
    preferences: UserPreferences
