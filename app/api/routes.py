from fastapi import APIRouter, File, HTTPException, UploadFile, Depends, Form
from fastapi.responses import Response

from app.api.dependencies import get_gemini_service, get_external_service
from app.schemas.gemini_response import GeminiAnalysisResponse
from app.services.gemini_service import GeminiService

from app.models.vision_model import VisionModel
from app.schemas.response import ImageAnalysisResponse
from app.services.image_analyzer import ImageAnalyzer

from app.api.dependencies import get_llava_service
from app.schemas.llava_response import LlavaAnalysisResponse
from app.services.llava_service import LlavaService
from app.services.external_service import ExternalService
import httpx


router = APIRouter()


vision_model = VisionModel()

analyzer = ImageAnalyzer(
    vision_model
)


@router.post(
    "/analyze",
    response_model=ImageAnalysisResponse
)
async def analyze_image(
    file: UploadFile = File(...)
):
    allowed_types = {
        "image/jpeg",
        "image/png",
        "image/webp",
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Formato de imagen no soportado"
        )

    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="El archivo está vacío"
        )

    try:
        result = analyzer.analyze(image_bytes)

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="No se pudo procesar la imagen"
        )

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        **result,
    }

@router.post("/analyze/rendered")
async def analyze_rendered_image(
    file: UploadFile = File(...),
):
    allowed_types = {
        "image/jpeg",
        "image/png",
        "image/webp",
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Formato de imagen no soportado",
        )

    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="El archivo está vacío",
        )

    try:
        result = analyzer.analyze(image_bytes)

        rendered = analyzer.render(
            image_bytes,
            result["people"],
        )

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"No se pudo procesar la imagen: {exc}",
        )

    return Response(
        content=rendered,
        media_type="image/jpeg",
    )


@router.post(
    "/analyze/gemini",
    response_model=GeminiAnalysisResponse,
)
async def analyze_with_gemini(
    prompt: str,
    file: UploadFile = File(...),
    gemini_service: GeminiService = Depends(
        get_gemini_service
    ),
):
    allowed_types = {
        "image/jpeg",
        "image/png",
        "image/webp",
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Formato de imagen no soportado",
        )

    if not prompt.strip():
        raise HTTPException(
            status_code=400,
            detail="El prompt no puede estar vacío",
        )

    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="El archivo está vacío",
        )

    try:

        result = gemini_service.analyze_image(
            image_bytes=image_bytes,
            mime_type=file.content_type,
            prompt=prompt,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=f"Error al consultar Gemini: {exc}",
        )

    return {
        "filename": file.filename,
        "prompt": prompt,
        "response": result,
    }


@router.post(
    "/analyze/llava",
    response_model=LlavaAnalysisResponse,
)
async def analyze_with_llava(
    prompt: str = Form(...),
    file: UploadFile = File(...),
    llava_service: LlavaService = Depends(
        get_llava_service
    ),
):
    allowed_types = {
        "image/jpeg",
        "image/png",
        "image/webp",
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Formato de imagen no soportado",
        )

    if not prompt.strip():
        raise HTTPException(
            status_code=400,
            detail="El prompt no puede estar vacío",
        )

    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="El archivo está vacío",
        )

    try:

        result = llava_service.analyze_image(
            image_bytes=image_bytes,
            prompt=prompt,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=f"Error al consultar LLaVA: {exc}",
        )

    return {
        "filename": file.filename,
        "prompt": prompt,
        "analysis": result,
    }

@router.post("/analyze/external")
async def analyze_with_external_service(
    prompt: str = Form(...),
    file: UploadFile = File(...),
    external_service: ExternalService = Depends(
        get_external_service
    ),
):
    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="El archivo está vacío",
        )

    try:

        result = await external_service.analyze_image(
            image_bytes=image_bytes,
            filename=file.filename or "image.jpg",
            content_type=file.content_type or "image/jpeg",
            prompt=prompt,
        )

    except httpx.HTTPStatusError as exc:

        raise HTTPException(
            status_code=502,
            detail=(
                "El servicio externo respondió "
                f"con HTTP {exc.response.status_code}"
            ),
        )

    except httpx.RequestError as exc:

        raise HTTPException(
            status_code=502,
            detail=(
                "No se pudo conectar con "
                "el servicio externo"
            ),
        )

    return result

@router.post("/analyze/camera")
async def analyze_camera(
    prompt: str = Form(...),
    file: UploadFile = File(...),
    llava_service: LlavaService = Depends(
        get_llava_service
    ),
):

    if file.content_type not in {
        "image/jpeg",
        "image/png",
        "image/webp",
    }:

        raise HTTPException(
            status_code=400,
            detail="Formato de imagen no soportado",
        )

    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="La imagen está vacía",
        )

    try:
        result = llava_service.analyze_image(
            image_bytes=image_bytes,
            prompt=prompt,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Error al consultar LLaVA: {exc}",
        )

    return {
        "filename": file.filename,
        "prompt": prompt,
        "analysis": result,
    }

