import time
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate, FeedbackResponse

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
    HTTPException,
)

from services.llava_sin_validacion_service import (
    LlavaSinValidacionService,
)

from schemas.api_llava_response import (
    ImageAnalysisResponse,
)

from app.api.dependencies import (
    get_llava_service_sin_val,
)


router = APIRouter(
    prefix="/api/v1",
    tags=["API"],
)


@router.post(
    "/analyze",
    response_model=ImageAnalysisResponse,
)
async def analyze_image(
    file: UploadFile = File(...),
    prompt: str = Form(...),
    llava_service: LlavaSinValidacionService = Depends(
        get_llava_service_sin_val
    ),
):

    start_time = time.perf_counter()

    if not prompt.strip():

        raise HTTPException(
            status_code=400,
            detail="El prompt no puede estar vacío",
        )

    allowed_types = {
        "image/jpeg",
        "image/png",
        "image/webp",
    }

    if file.content_type not in allowed_types:

        raise HTTPException(
            status_code=400,
            detail="El archivo debe ser una imagen JPEG, PNG o WEBP",
        )

    try:

        image_bytes = await file.read()

        if not image_bytes:

            raise HTTPException(
                status_code=400,
                detail="La imagen está vacía",
            )

        result = llava_service.analyze_image(
            image_bytes=image_bytes,
            prompt=prompt,
        )

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=f"Error al consultar LLaVA: {exc}",
        )

    total_time = time.perf_counter() - start_time

    return {
        "success": True,
        "analysis": result["analysis"],
        "id_peticion": result["id_peticion"],
        "ollama_time": result["elapsed_time"],
        "total_time": round(total_time, 10),
    }


@router.post(
    "/analyze/feedback",
    response_model=FeedbackResponse,
)
async def crear_feedback(
    id_peticion: str = Form(...),
    edad: str = Form(...),
    emocion: str = Form(...),
    llava_service: LlavaSinValidacionService = Depends(
        get_llava_service_sin_val
    ),
):
    print("Entra a post")
    
    try:
        result = llava_service.feedback(
            id_peticion=id_peticion,
            coincide_edad=edad,
            coincide_emocion=emocion
        )

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=f"Error al enviar el feedback: {exc}",
        )

    return {
        "id": result["id"],
        
    }