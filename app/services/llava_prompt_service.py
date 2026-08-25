import ollama
import time

class LlavaPromptService:

    def __init__(
        self,
        model: str = "llava",
    ):
        self.model = model

        print(
            f">>> LlavaPromptService inicializado con modelo: {self.model}"
        )

        print("LLaVA: Entra")

    def analyze(
        self,
        prompt: str,
    ) -> dict:

        print("========== ENTRE A analyze() ==========")
        print("PROMPT:", prompt)

        structured_prompt = f"""
REGLAS:

- Responde en español.
- No agregues explicaciones.
- No utilices Markdown.

PROMPT DEL USUARIO:
{prompt}
"""

        start = time.perf_counter()

        print("LLaVA: antes de petición")
        print("LLaVA prompt:", prompt)

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": structured_prompt,
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