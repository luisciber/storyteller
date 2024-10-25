import functools
from operator import add
from typing import Annotated, Optional

from langchain.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

from app.core.config import settings
from app.prompts import CHAPTER_DEVELOPMENT_PROMPT, STORY_OUTLINE_PROMPT


# Modelos Pydantic para la estructura de datos
class StoryOutline(BaseModel):
    premise: str = Field(description="La premisa principal de la historia")
    num_chapters: int = Field(
        description="El número total de capítulos en la historia"
    )
    chapter_titles: list[str] = Field(
        description="Lista de títulos para cada capítulo de la historia"
    )


class ChapterContent(BaseModel):
    content: str = Field(description="El contenido detallado del capítulo")
    image_description: str = Field(
        description="Descripción detallada para la generación de una imagen clave del capítulo"
    )


class Chapter(ChapterContent):
    title: str


class ImageDescription(BaseModel):
    prompt: str
    style_guidance: str


# Nuevo modelo para las preferencias del usuario
class UserPreferences(BaseModel):
    genre: str = Field(description="El género literario de la historia")
    length: str = Field(
        description="La longitud deseada de la historia (corta, media, larga)"
    )
    style: str = Field(description="El estilo de escritura deseado")
    themes_to_include: list[str] = Field(
        description="Lista de temas que deben incluirse en la historia"
    )
    themes_to_avoid: list[str] = Field(
        description="Lista de temas que deben evitarse en la historia")
    art_style: str = Field(
        description="El estilo artístico deseado para las imágenes"
    )


# Configuración del modelo de lenguaje
claude_llm = ChatAnthropic(
    model="claude-3-5-sonnet-latest", api_key=settings.anthropic_api_key
)

openai_llm = ChatOpenAI(
    model="gpt-4o", api_key=settings.openai_api_key
)

# Estado del grafo


class GraphState(TypedDict):
    user_preferences: UserPreferences
    outline: Optional[StoryOutline]
    chapters: Annotated[list[Chapter], add]


# Nodos del grafo


def generate_outline(state: GraphState) -> GraphState:
    prompt = ChatPromptTemplate.from_template(STORY_OUTLINE_PROMPT)
    chain = prompt | claude_llm.with_structured_output(StoryOutline)
    outline = chain.invoke(state['user_preferences'].model_dump())
    return {"outline": outline}


async def develop_chapters(state: GraphState) -> GraphState:
    outline = state['outline']

    develop_chapter_nodes = [functools.partial(
        develop_chapter, current_chapter=chapter_number
    ) for chapter_number in range(outline.num_chapters)]

    builder = StateGraph(GraphState)

    for index in range(outline.num_chapters):
        builder.add_node(
            f"develop_chapter_{index}", develop_chapter_nodes[index]
        ).add_edge(
            START, f"develop_chapter_{index}"
        ).add_edge(
            f"develop_chapter_{index}", END
        )

    graph = builder.compile()
    result = await graph.ainvoke(state)

    return result


def develop_chapter(state: GraphState, current_chapter: int) -> GraphState:
    prompt = ChatPromptTemplate.from_template(CHAPTER_DEVELOPMENT_PROMPT)
    chain = prompt | openai_llm.with_structured_output(ChapterContent)
    chapter_content = chain.invoke({
        "chapter_title": state['outline'].chapter_titles[current_chapter],
        "premise": state['outline'].premise,
        "user_preferences": state['user_preferences'].model_dump()
    })
    return {"chapters": [
        Chapter(
            title=state['outline'].chapter_titles[current_chapter],
            content=chapter_content.content,
            image_description=chapter_content.image_description
        )
    ], "current_chapter": current_chapter + 1}


# Configuración del grafo
workflow = StateGraph(GraphState)

# Agregar nodos
workflow.add_node("generate_outline", generate_outline)
workflow.add_node("develop_chapters", develop_chapters)

# Definir el flujo
workflow.set_entry_point("generate_outline")
workflow.add_edge("generate_outline", "develop_chapters")

# Compilar el grafo
story_generation_app = workflow.compile()

# Función para iniciar el proceso de generación de historia


async def generate_story(user_preferences: UserPreferences) -> GraphState:
    initial_state: GraphState = {
        "user_preferences": user_preferences,
        "outline": None,
        "current_chapter": 0,
        "chapters": []
    }
    final_state = await story_generation_app.ainvoke(initial_state)
    return final_state
