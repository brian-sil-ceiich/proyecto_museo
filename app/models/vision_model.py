from io import BytesIO

from PIL import Image
from ultralytics import YOLO

from app.models.base import VisionModelInterface


class VisionModel(VisionModelInterface):

    def __init__(self):
        self.model = YOLO("yolo26n.pt")

    def analyze(self, image_bytes: bytes) -> dict:

        image = Image.open(
            BytesIO(image_bytes)
        ).convert("RGB")

        results = self.model.predict(
            source=image,
            verbose=False,
            conf=0.25,
        )

        result = results[0]

        people = []

        if result.boxes is not None:

            for box in result.boxes:

                class_id = int(box.cls[0])
                confidence = float(box.conf[0])

                class_name = result.names[class_id]

                if class_name != "person":
                    continue

                coordinates = box.xyxy[0].tolist()

                people.append(
                    {
                        "confidence": round(
                            confidence,
                            4,
                        ),
                        "box": {
                            "x1": round(
                                coordinates[0],
                                2,
                            ),
                            "y1": round(
                                coordinates[1],
                                2,
                            ),
                            "x2": round(
                                coordinates[2],
                                2,
                            ),
                            "y2": round(
                                coordinates[3],
                                2,
                            ),
                        },
                    }
                )

        return {
            "person_detected": len(people) > 0,
            "number_of_people": len(people),
            "people": people,
        }