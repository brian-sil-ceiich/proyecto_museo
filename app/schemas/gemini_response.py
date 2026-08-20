from pydantic import BaseModel


class GeminiAnalysisResponse(BaseModel):
    filename: str
    prompt: str
    response: str