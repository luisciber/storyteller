CHAPTER_DEVELOPMENT_PROMPT = """
Desarrolla el siguiente capítulo de la historia basándote en la información proporcionada:

Título de la historia: {title}
Título del capítulo: {chapter_title}
Premisa de la historia: {premise}
Preferencias del usuario: {user_preferences}

Genera el contenido detallado del capítulo, incluyendo diálogos y descripciones. 
También, proporciona una descripción para una imagen que represente una escena clave del capítulo.

Formato de salida:
{{
    "content": "Contenido detallado del capítulo...",
    "image_description": "Descripción detallada para la generación de una imagen clave del capítulo"
}}
"""
