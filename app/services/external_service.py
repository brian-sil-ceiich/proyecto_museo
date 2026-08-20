import os

import httpx


class ExternalService:

    def __init__(
        self,
        base_url: str | None = None,
    ):
        self.base_url = (
            base_url
            or os.getenv("EXTERNAL_SERVICE_URL")
        )

        if not self.base_url:
            raise ValueError(
                "EXTERNAL_SERVICE_URL no está configurada"
            )

    async def analyze_image(
        self,
        image_bytes: bytes,
        filename: str,
        content_type: str,
        prompt: str,
    ) -> dict:

        url = f"{self.base_url}/analyze"

        files = {
            "file": (
                filename,
                image_bytes,
                content_type,
            )
        }

        data = {
            "prompt": prompt
        }

        async with httpx.AsyncClient(
            timeout=120.0
        ) as client:

            response = await client.post(
                url,
                files=files,
                data=data,
            )

            response.raise_for_status()

            return response.json()