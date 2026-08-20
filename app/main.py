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
        "app/static/index.html"
    )

@app.get("/camera")
async def camera_page():

    return FileResponse(
        "app/static/camera.html"
    )
