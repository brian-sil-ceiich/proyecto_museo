import ollama
import time


class DeepSeekPromptService:

    def __init__(
        self,
        model: str = "deepseek-llm:7b",
    ):
        self.model = model

        print(
            f">>> DeepSeekPromptService inicializado con modelo: {self.model}"
        )

    def analyze(
        self,
        prompt: str,
    ) -> dict:

        structured_prompt = f"""
        REGLAS:
        
        - Responde en español.
        - Responde en menos de 20 segundos.
        - No agregues explicaciones.
        - No utilices Markdown.
        
        PROMPT DEL USUARIO:
        {prompt}
        """

        start = time.perf_counter()

        print("DeepSeek: antes de petición")

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
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

        print("DeepSeek: Ollama respondió")

        # print(
        #     "DeepSeek respuesta:",
        #     response.message.content
        # )

        return {
            "analysis": response.message.content,
            "elapsed_time": round(elapsed_time, 10),
        }