import ollama
import time

class LlavaSinValidacionService:

    def __init__(
        self,
        model: str = "llava",
    ):
        self.model = model

        print(
            f">>> LlavaSinValidacionService inicializado con modelo: {self.model}"
        )

    def analyze_image(
        self,
        image_bytes: bytes,
        prompt: str,
    ) -> str:

        structured_prompt = """
Analiza la imagen y determina las siguientes características
de la persona visible:

1. EDAD
   - Estima el rango de edad en años que aparenta tener la persona, quiero que me lo digas en años.

2. EMOCION
   - Determina la emoción que parece expresar la persona
     mediante su expresión facial.
   - No respondas neutral.

REGLAS:

- Responde en español.
- No agregues explicaciones.
- No utilices Markdown.
- Responde únicamente con la edad y la emoción.
"""
        start = time.perf_counter()
        print("LLaVA: antes de petición")

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
            options={
                "temperature": 0,
            },
        )
        elapsed_time = time.perf_counter() - start

        print(
            f"Tiempo de inferencia: {elapsed_time:.10f} segundos"
        )

        print("LLaVA: Ollama respondió")

        print(
            "LLaVA respuesta:",
            response.message.content
        )

        return {
            "analysis": response.message.content,
            "elapsed_time": round(elapsed_time, 10),
        }