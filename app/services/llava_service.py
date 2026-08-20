from app.schemas.llava_response import LlavaAnalysis

import json

import ollama

# --{prompt}
class LlavaService:

    def __init__(
        self,
        model: str = "llava",
    ):
        self.model = model

    def analyze_image(
        self,
        image_bytes: bytes,
        prompt: str,
    ) -> dict:
        
        structured_prompt = f"""

Analiza la imagen y responde exclusivamente utilizando el esquema JSON proporcionado.

La aplicación necesita identificar dos características de la persona visible:

1. EDAD
   - Estima únicamente el rango de edad que aparenta tener la persona.
   - No intentes determinar la edad real.
   - Si la imagen no permite realizar una estimación razonable, utiliza el rango que corresponda a la mejor estimación visual posible.

2. EMOCION
   - Determina la emoción que parece expresar la persona mediante su expresión facial.
   - No quiero que respondas neutral

REGLAS:
- Responde en español.
- No agregues explicaciones.
- No agregues texto fuera del JSON.
- No utilices Markdown.
- No inventes información.
- Devuelve únicamente los campos definidos en el esquema.

"""

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": structured_prompt,
                    "images": [
                        image_bytes,
                    ],
                }
            ],
            format=LlavaAnalysis.model_json_schema(),
            options={
                "temperature": 0,
            },
        )

        content = response.message.content

        try:
            return LlavaAnalysis.model_validate_json(
                response.message.content
            )

        except json.JSONDecodeError as exc:
            raise ValueError(
                f"LLaVA no devolvió JSON válido: {content}"
            ) from exc