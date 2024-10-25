IMAGE_GENERATION_PROMPT = """
Genera una descripción detallada para crear una imagen basada en el siguiente contexto:

Escena: {scene_description}
Personajes involucrados: {characters}
Atmósfera: {atmosphere}
Estilo artístico: {art_style}

La descripción debe ser lo suficientemente detallada para que un modelo de generación de imágenes pueda crear una ilustración precisa y coherente con la historia.

Formato de salida:
{{
    "prompt": "Descripción detallada para la generación de imagen",
    "style_guidance": "Instrucciones adicionales sobre el estilo y la composición"
}}
"""
