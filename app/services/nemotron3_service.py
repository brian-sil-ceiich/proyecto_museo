import ollama


class Nemotron3Service:

    def __init__(
        self,
        model: str = "nemotron3:33b",
    ):
        self.model = model

    def analyze_image(
        self,
        image_bytes: bytes,
        prompt: str,
    ) -> str:

        analysis_prompt = """
Analiza la imagen.

Necesito identificar dos características de la persona visible:

1. EDAD
   Estima el rango de edad que aparenta tener la persona.
   No intentes determinar su edad real.

2. ROPA
   Describe el atuendo de la persona.

REGLAS:

- Responde en español.
- No des explicaciones.
- Responde únicamente con la edad estimada y el atuendo.
"""

# 2. EMOCION
#    Determina la emoción que parece expresar mediante
#    su expresión facial.

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": analysis_prompt,
                    "images": [
                        image_bytes,
                    ],
                }
            ],
            options={
                "temperature": 0,
            },
        )

        return response.message.content