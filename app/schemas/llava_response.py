from pydantic import BaseModel, Field


class DetectedElement(BaseModel):
    name: str
    description: str


class LlavaAnalysis(BaseModel):
    age: str = Field(
        description="Tell me the estimated Age of the person in a range of decades"
    )
    emocion: str 

#"Tell me the emotion of the person, avoid the use of neutral"
# = Field(
#         description="Tell me the emotion of the person, avoid the use of neutral" #described as happy, sad, cheerful, or angry
#     )


class LlavaAnalysisResponse(BaseModel):
    filename: str
    prompt: str
    analysis: LlavaAnalysis

class LlavaTextResponse(BaseModel):
    filename: str
    prompt: str
    analysis: str
    ollama_time: float
    total_time: float


#     from pydantic import BaseModel, Field


# class DetectedElement(BaseModel):
#     name: str
#     description: str


# class LlavaAnalysis(BaseModel):
#     edad: str = Field(
#         description="Indicame la edad estimada de la persona en un rago de décadas"
#     )
#     emocion: str = Field(
#         description="Indicame la emoción que percibes que tiene la persona de la imagen" #described as happy, sad, cheerful, or angry
#     )


# class LlavaAnalysisResponse(BaseModel):
#     filename: str
#     prompt: str
#     analysis: LlavaAnalysis