from app.models.base import VisionModelInterface


class FakeVisionModel(VisionModelInterface):

    def analyze(
        self,
        image_bytes: bytes,
    ) -> dict:

        return {
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