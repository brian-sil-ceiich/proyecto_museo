from io import BytesIO

from PIL import Image

from app.services.image_analyzer import ImageAnalyzer
from tests.fakes import FakeVisionModel


def create_test_image():

    image = Image.new(
        "RGB",
        (1920, 1080),
        "white",
    )

    buffer = BytesIO()

    image.save(
        buffer,
        format="JPEG",
    )

    buffer.seek(0)

    return buffer.read()


def test_image_analyzer():

    vision_model = FakeVisionModel()

    analyzer = ImageAnalyzer(
        vision_model
    )

    image_bytes = create_test_image()

    result = analyzer.analyze(
        image_bytes
    )

    assert result["width"] == 1920
    assert result["height"] == 1080
    assert result["image_quality"] == "good"

    assert result["person_detected"] is True
    assert result["number_of_people"] == 1

    assert len(result["people"]) == 1