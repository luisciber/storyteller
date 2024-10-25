from app.models.base import Model
from app.story_generation.story_flow import Chapter


class Story(Model):
    title: str
    premise: str
    chapters: list[Chapter]
