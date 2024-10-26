import uuid

import replicate
import replicate.helpers

from app.services.bucket_service import BucketService

bucket_service = BucketService()


async def generate_image(prompt: str) -> str:
    response: list[replicate.helpers.FileOutput] = replicate.run(
        "black-forest-labs/flux-schnell",
        input={
            "prompt": prompt,
            "go_fast": True,
            "megapixels": "1",
            "num_outputs": 1,
            "aspect_ratio": "16:9",
            "output_format": "webp",
            "output_quality": 80,
            "num_inference_steps": 4
        }
    )

    file = response[0]
    data = file.read()
    path = f"images/{uuid.uuid4()}.webp"
    url = await bucket_service.upload_file(data, path)

    return url
