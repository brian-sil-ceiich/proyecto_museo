from pydantic import BaseModel


class ImageAnalysisResponse(BaseModel):
    success: bool
    analysis: str
    ollama_time: float
    total_time: float