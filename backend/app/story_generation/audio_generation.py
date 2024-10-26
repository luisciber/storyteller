import base64
import io
import json
import uuid

import websockets
from pydub import AudioSegment

from app.core.config import settings
from app.services.bucket_service import BucketService

# Configura la URL del WebSocket y la API key
URL = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01"
api_key = settings.openai_api_key

NARRATOR_PROMPT = "Por favor cuenta esta historia: "

bucket_service = BucketService()


async def generate_audio(history: str):
    event_id = str(uuid.uuid4())

    headers = {
        "Authorization": f"Bearer {api_key}",
        "OpenAI-Beta": "realtime=v1",
    }

    async with websockets.connect(URL, extra_headers=headers) as ws:
        # Envía una solicitud para que el modelo responda con texto
        message = {
            "event_id": event_id,
            "type": "response.create",
            "response": {
                "modalities": ["audio", "text"],
                "instructions": f"{NARRATOR_PROMPT}: {history}",
                "voice": "alloy",
                "output_audio_format": "pcm16",
                "temperature": 0.7,
                "max_output_tokens": 4096,
            }
        }

        await ws.send(json.dumps(message))
        audio_chunks: list[AudioSegment] = []

        async for response in ws:
            data = json.loads(response)
            if data["type"] == 'response.audio.delta':
                audio_data = base64.b64decode(data['delta'])
                audio_chunk = AudioSegment(
                    data=audio_data,
                    sample_width=2,
                    frame_rate=24000,
                    channels=1
                )
                audio_chunks.append(audio_chunk)
            elif data["type"] == 'response.done':
                break

        buffer = io.BytesIO()
        combined_audio = sum(audio_chunks)
        combined_audio.export(buffer, format="wav")
        buffer.seek(0)

        path = f'audios/{event_id}.wav'
        audio_url = await bucket_service.upload_file(buffer.getvalue(), path)

        return audio_url
