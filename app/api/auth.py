import os

from fastapi import (
    Header,
    HTTPException,
)


def verify_api_key(
    x_api_key: str | None = Header(default=None),
):
    expected_api_key = os.getenv(
        "LLAVA_API_KEY"
    )

    if not expected_api_key:
        raise RuntimeError(
            "LLAVA_API_KEY no está configurada"
        )

    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="API Key requerida",
        )

    if x_api_key != expected_api_key:
        raise HTTPException(
            status_code=403,
            detail="API Key inválida",
        )

    return True