from pydantic import BaseModel


class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float


class PersonDetection(BaseModel):
    confidence: float
    box: BoundingBox


class ImageAnalysisResponse(BaseModel):
    filename: str
    content_type: str
    width: int
    height: int
    person_detected: bool
    number_of_people: int
    image_quality: str
    people: list[PersonDetection]