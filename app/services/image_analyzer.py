from io import BytesIO

from PIL import Image

from app.models.base import VisionModelInterface
from app.services.image_renderer import ImageRenderer


class ImageAnalyzer:

    def __init__(
        self,
        vision_model: VisionModelInterface,
    ):
        self.vision_model = vision_model
        self.renderer = ImageRenderer()

    def analyze(
        self,
        image_bytes: bytes,
    ) -> dict:

        image = Image.open(
            BytesIO(image_bytes)
        )

        width, height = image.size

        quality = self._calculate_quality(
            width,
            height,
        )

        vision_result = self.vision_model.analyze(
            image_bytes
        )

        return {
            "width": width,
            "height": height,
            "image_quality": quality,
            **vision_result,
        }

    def render(
        self,
        image_bytes: bytes,
        detections: list[dict],
    ) -> bytes:

        return self.renderer.draw_detections(
            image_bytes,
            detections,
        )

    def _calculate_quality(
        self,
        width: int,
        height: int,
    ) -> str:

        pixels = width * height

        if pixels >= 1920 * 1080:
            return "good"

        if pixels >= 1280 * 720:
            return "medium"

        return "low"