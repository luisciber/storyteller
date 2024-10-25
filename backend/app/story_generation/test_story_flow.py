import asyncio
import json
from datetime import datetime

from app.story_generation.story_flow import (GraphState, UserPreferences,
                                             story_generation_app)


async def test_story_generation():
    # Crear preferencias de usuario de ejemplo
    user_preferences = UserPreferences(
        genre="Ciencia ficción",
        length="media",
        style="Descriptivo",
        themes_to_include=["Exploración espacial", "Inteligencia artificial"],
        themes_to_avoid=["Violencia gráfica"],
        art_style="Futurista"
    )

    # Configurar el estado inicial
    initial_state: GraphState = {
        "user_preferences": user_preferences,
        "outline": None,
        "current_chapter": 0,
        "chapter_content": None,
        "image_descriptions": []
    }

    # Ejecutar el grafo y mostrar actualizaciones de estado
    results = []
    async for event in story_generation_app.astream(initial_state, stream_mode="values"):
        print(event)
        with open(
            f"data/story_generation_state_{
                datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "w", encoding="utf-8"
        ) as f:
            json.dump(event, f, indent=2, default=str)
        results.append(event)

    # Guardar los resultados en un archivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/story_generation_results_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"Resultados guardados en {filename}")

if __name__ == "__main__":
    asyncio.run(test_story_generation())
