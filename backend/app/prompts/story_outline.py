STORY_OUTLINE_PROMPT = """
Crea un esquema narrativo para una historia basada en las siguientes preferencias del usuario:
Género: {genre}
Longitud: {length}
Estilo: {style}
Temas a incluir: {themes_to_include}
Temas a evitar: {themes_to_avoid}

El esquema debe incluir:
1. Premisa principal
2. Número de capítulos
3. Títulos de los capítulos

Formato de salida:
{{
    "title": "Título de la historia",
    "image_description": "Descripción detallada para la generación de una imagen clave de la historia",
    "premise": "Breve descripción de la premisa principal",
    "num_chapters": número_de_capítulos,
    "chapter_titles": ["Título del capítulo 1", "Título del capítulo 2", ...]
}}
"""
