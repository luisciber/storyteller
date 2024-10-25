
from operator import add
from typing import Annotated, Optional

from langchain.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from langgraph.graph import END, StateGraph
from pydantic import BaseModel
from typing_extensions import TypedDict

from app.core.config import settings
from app.prompts import CHAPTER_DEVELOPMENT_PROMPT, STORY_OUTLINE_PROMPT


# Modelos Pydantic para la estructura de datos
class StoryOutline(BaseModel):
    premise: str
    num_chapters: int
    chapter_titles: list[str]


class ChapterContent(BaseModel):
    content: str
    image_description: str


class ImageDescription(BaseModel):
    prompt: str
    style_guidance: str


# Nuevo modelo para las preferencias del usuario
class UserPreferences(BaseModel):
    genre: str
    length: str
    style: str
    themes_to_include: list[str]
    themes_to_avoid: list[str]
    art_style: str


# Configuración del modelo de lenguaje
claude_llm = ChatAnthropic(
    model="claude-3-5-sonnet-latest", api_key=settings.anthropic_api_key
)

# Estado del grafo


class GraphState(TypedDict):
    user_preferences: UserPreferences
    outline: Optional[StoryOutline]
    current_chapter: int
    chapters: Annotated[list[ChapterContent], add]

# Nodos del grafo


def generate_outline(state: GraphState) -> GraphState:
    prompt = ChatPromptTemplate.from_template(STORY_OUTLINE_PROMPT)
    chain = prompt | claude_llm.with_structured_output(StoryOutline)
    outline = chain.invoke(state['user_preferences'].model_dump())
    return {"outline": outline}


def develop_chapter(state: GraphState) -> GraphState:
    current_chapter = state['current_chapter']
    prompt = ChatPromptTemplate.from_template(CHAPTER_DEVELOPMENT_PROMPT)
    chain = prompt | claude_llm.with_structured_output(ChapterContent)
    chapter_content = chain.invoke({
        "chapter_title": state['outline'].chapter_titles[current_chapter],
        "premise": state['outline'].premise,
        "user_preferences": state['user_preferences'].model_dump()
    })
    return {"chapters": [chapter_content], "current_chapter": current_chapter + 1}


def should_continue(state: GraphState) -> str:
    if state['current_chapter'] < state['outline'].num_chapters:
        return "develop_chapter"
    return END


# Configuración del grafo
workflow = StateGraph(GraphState)

# Agregar nodos
workflow.add_node("generate_outline", generate_outline)
workflow.add_node("develop_chapter", develop_chapter)

# Definir el flujo
workflow.set_entry_point("generate_outline")
workflow.add_edge("generate_outline", "develop_chapter")
workflow.add_conditional_edges(
    "develop_chapter",
    should_continue
)

# Compilar el grafo
story_generation_app = workflow.compile()

# Función para iniciar el proceso de generación de historia


async def generate_story(user_preferences: UserPreferences):
    initial_state: GraphState = {
        "user_preferences": user_preferences,
        "outline": None,
        "current_chapter": 0,
        "chapters": []
    }
    final_state = await story_generation_app.ainvoke(initial_state)
    return final_state
