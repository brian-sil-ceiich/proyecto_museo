import os

from fastapi import HTTPException

from app.services.gemini_service import GeminiService
from app.services.llava_service import LlavaService
from app.services.external_service import ExternalService
from app.services.llava_sin_validacion_service import LlavaSinValidacionService
from app.services.llava_prompt_service import LlavaPromptService
from app.services.deepseek_prompt_service import DeepSeekPromptService


def get_llava_service() -> LlavaService:

    return LlavaService(
        model="llava",
    )


def get_llava_service_sin_val() -> LlavaSinValidacionService:

    return LlavaSinValidacionService(
        model="llava",
    )

def get_llava_prompt() -> LlavaPromptService:

    return LlavaPromptService(
        model="llava",
    )

def get_gemini_service() -> GeminiService:

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY no está configurada",
        )

    return GeminiService(
        api_key=api_key,
    )

def get_external_service() -> ExternalService:

    return ExternalService()

def get_deepseek_prompt():
    return DeepSeekPromptService(
        model="deepseek-llm:7b"
    )