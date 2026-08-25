from pydantic import BaseModel, Field

class DeepSeekPromptResponse(BaseModel):
    prompt: str
    analysis: str
    ollama_time: float
    total_time: float