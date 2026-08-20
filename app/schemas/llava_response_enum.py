from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class AgeRange(str, Enum):
    MENOR_13 = "0-12"
    ADOLESCENTE = "13-17"
    JOVEN = "18-24"
    ADULTO_JOVEN = "25-34"
    ADULTO = "35-44"
    ADULTO_MADURO = "45-54"
    MAYOR = "55-64"
    ADULTO_MAYOR = "65+"


class Emotion(str, Enum):
    FELIZ = "feliz"
    TRISTE = "triste"
    ALEGRE = "alegre"
    ENOJADO = "enojado"
    DESCONOCIDO = "desconocido"


class LlavaAnalysis(BaseModel):
    age: AgeRange = Field(
        description="Rango aproximado de edad aparente de la persona."
    )

    emotion: Emotion = Field(
        description="Indica que estado de anímo tiene la persona"
    )


class LlavaAnalysisResponse(BaseModel):
    filename: str
    prompt: str
    analysis: LlavaAnalysis