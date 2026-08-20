from abc import ABC, abstractmethod


class VisionModelInterface(ABC):

    @abstractmethod
    def analyze(self, image_bytes: bytes) -> dict:
        pass