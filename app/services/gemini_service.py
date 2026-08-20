from google import genai
from google.genai import types


class GeminiService:

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-3.6-flash",
    ):
        self.client = genai.Client(
            api_key=api_key
        )

        self.model = model

    def analyze_image(
        self,
        image_bytes: bytes,
        mime_type: str,
        prompt: str,
    ) -> str:

        response = self.client.models.generate_content(
            model=self.model,
            contents=[
                types.Part.from_text(
                    text=prompt
                ),
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type,
                ),
            ],
        )

        return response.text