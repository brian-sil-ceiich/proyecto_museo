from io import BytesIO

from fastapi.testclient import TestClient
from PIL import Image

from app.main import app
from app.services.image_analyzer import ImageAnalyzer


client = TestClient(app)


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

    return buffer


def fake_analyze(self, image_bytes):
    return {
        "width": 1920,
        "height": 1080,
        "image_quality": "good",
        "person_detected": True,
        "number_of_people": 1,
        "people": [
            {
                "confidence": 0.95,
                "box": {
                    "x1": 100.0,
                    "y1": 100.0,
                    "x2": 500.0,
                    "y2": 900.0,
                },
            }
        ],
    }


def test_analyze_image(monkeypatch):

    monkeypatch.setattr(
        ImageAnalyzer,
        "analyze",
        fake_analyze,
    )

    image = create_test_image()

    response = client.post(
        "/analyze",
        files={
            "file": (
                "test.jpg",
                image,
                "image/jpeg",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == "test.jpg"
    assert data["width"] == 1920
    assert data["height"] == 1080
    assert data["image_quality"] == "good"
    assert data["person_detected"] is True
    assert data["number_of_people"] == 1
    assert len(data["people"]) == 1