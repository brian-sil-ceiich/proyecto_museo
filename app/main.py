from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.routes import router


app = FastAPI(
    title="Image Analysis API",
    description="API modular para análisis de imágenes",
    version="1.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)

app.include_router(router)

@app.get("/")
async def home():
    return FileResponse(
        "app/static/home.html"
    )

@app.get("/index")
async def home():
    return FileResponse(
        "app/static/index.html"
    )

@app.get("/camera")
async def camera_page():

    return FileResponse(
        "app/static/camera.html"
    )

@app.get("/nemotron3")
async def camera_page():

    return FileResponse(
        "app/static/nemotron3.html"
    )

@app.get("/llava_sin_val")
async def camera_page():

    return FileResponse(
        "app/static/llava_sin_validacion.html"
    )

@app.get("/llava_prompt")
async def camera_page():

    return FileResponse(
        "app/static/llava_prompt.html"
    )

@app.get("/deepseeker_prompt")
async def camera_page():

    return FileResponse(
        "app/static/deepseeker_prompt.html"
    )
