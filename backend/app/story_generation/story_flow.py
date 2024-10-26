import asyncio
import functools
from operator import add
from typing import Annotated, Optional

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

from app.core.config import settings
from app.prompts import (CHAPTER_DEVELOPMENT_PROMPT, MAIN_IMAGE_PROMPT,
                         STORY_OUTLINE_PROMPT)
from app.story_generation.audio_generation import generate_audio
from app.story_generation.image_generation import generate_image


# Modelos Pydantic para la estructura de datos
class StoryOutline(BaseModel):
    premise: str = Field(description="La premisa principal de la historia")
    num_chapters: int = Field(
        description="El número total de capítulos en la historia"
    )
    chapter_titles: list[str] = Field(
        description="Lista de títulos para cada capítulo de la historia"
    )
    title: str = Field(description="El título de la historia")


class ChapterContent(BaseModel):
    content: str = Field(description="El contenido detallado del capítulo")
    image_description: str = Field(
        description="""
Descripción detallada para la generación de una imagen clave del capítulo, 
la descripción debe ser en inglés y debe ser lo más detallada posible
        """
    )


class Chapter(ChapterContent):
    id: int = Field(description="El ID del capítulo")
    title: str = Field(description="El título del capítulo")
    image_url: Optional[str] = Field(
        description="La URL de la imagen del capítulo",
        default=None
    )
    audio_url: Optional[str] = Field(
        description="La URL del audio del capítulo",
        default=None
    )

# Preferencias del usuario


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


openai_llm = ChatOpenAI(
    model="gpt-4o", api_key=settings.openai_api_key
)

# Estado del grafo


class GraphState(TypedDict):
    user_preferences: UserPreferences
    outline: Optional[StoryOutline]
    main_image_url: Optional[str]
    chapters: Annotated[list[Chapter], add]


# Nodos del grafo


async def generate_outline(state: GraphState) -> GraphState:
    prompt = ChatPromptTemplate.from_template(STORY_OUTLINE_PROMPT)
    chain = prompt | openai_llm.with_structured_output(StoryOutline)
    outline: StoryOutline = await chain.ainvoke(
        state['user_preferences'].model_dump()
    )

    return {"outline": outline}


async def generate_main_image(state: GraphState) -> GraphState:
    outline = state['outline']
    main_image_prompt = ChatPromptTemplate.from_template(MAIN_IMAGE_PROMPT)
    main_image_chain = main_image_prompt | openai_llm | StrOutputParser()
    main_image_description = await main_image_chain.ainvoke({
        "title": outline.title,
        "premise": outline.premise
    })

    main_image_url = await generate_image(main_image_description)

    return {"main_image_url": main_image_url}


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


async def develop_chapter(state: GraphState, current_chapter: int) -> GraphState:
    prompt = ChatPromptTemplate.from_template(CHAPTER_DEVELOPMENT_PROMPT)
    chain = prompt | openai_llm.with_structured_output(ChapterContent)

    # Generate chapter content
    chapter_content: ChapterContent = await chain.ainvoke({
        "title": state['outline'].title,
        "chapter_title": state['outline'].chapter_titles[current_chapter],
        "premise": state['outline'].premise,
        "user_preferences": state['user_preferences'].model_dump()
    })

    # Generate image and audio in parallel
    image_task = asyncio.create_task(
        generate_image(chapter_content.image_description)
    )
    audio_task = asyncio.create_task(
        generate_audio(chapter_content.content)
    )

    image_url, audio_url = await asyncio.gather(image_task, audio_task)

    return {"chapters": [
        Chapter(
            id=current_chapter,
            title=state['outline'].chapter_titles[current_chapter],
            content=chapter_content.content,
            image_description=chapter_content.image_description,
            image_url=image_url,
            audio_url=audio_url
        )
    ]}


# Configuración del grafo
workflow = StateGraph(GraphState)

# Agregar nodos
workflow.add_node("generate_outline", generate_outline)
workflow.add_node("generate_main_image", generate_main_image)
workflow.add_node("develop_chapters", develop_chapters)

# Definir el flujo
workflow.set_entry_point("generate_outline")
workflow.add_edge("generate_outline", "develop_chapters")
workflow.add_edge("generate_outline", "generate_main_image")

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
    final_state: GraphState = await story_generation_app.ainvoke(initial_state)
    final_state['chapters'] = sorted(
        final_state['chapters'], key=lambda x: x.id
    )
    return final_state
