from io import BytesIO

from PIL import Image, ImageDraw


class ImageRenderer:

    def draw_detections(
        self,
        image_bytes: bytes,
        detections: list[dict],
    ) -> bytes:

        image = Image.open(
            BytesIO(image_bytes)
        ).convert("RGB")

        draw = ImageDraw.Draw(image)

        for detection in detections:

            box = detection["box"]

            x1 = box["x1"]
            y1 = box["y1"]
            x2 = box["x2"]
            y2 = box["y2"]

            confidence = detection["confidence"]

            draw.rectangle(
                (x1, y1, x2, y2),
                outline="red",
                width=4,
            )

            label = f"person {confidence:.2f}"

            draw.text(
                (x1, max(0, y1 - 20)),
                label,
                fill="red",
            )

        output = BytesIO()

        image.save(
            output,
            format="JPEG",
            quality=90,
        )

        return output.getvalue()