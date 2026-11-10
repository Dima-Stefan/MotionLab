"""Parametrii de detecție și validarea lor."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path

from .errors import InvalidParameterError, InvalidROIError, VideoFileError


@dataclass(frozen=True)
class ROI:
    x: int
    y: int
    w: int
    h: int

    def validate(self, frame_width: int, frame_height: int) -> None:
        if self.x < 0 or self.y < 0:
            raise InvalidROIError("Coordonatele ROI nu pot fi negative.")
        if self.w <= 0 or self.h <= 0:
            raise InvalidROIError("Lățimea și înălțimea ROI trebuie să fie pozitive.")
        if self.x + self.w > frame_width or self.y + self.h > frame_height:
            raise InvalidROIError(
                f"ROI ({self.x},{self.y},{self.w},{self.h}) depășește cadrul "
                f"({frame_width}x{frame_height})."
            )


@dataclass(frozen=True)
class DetectionParams:
    roi: ROI | None = None           # None = tot cadrul
    pixel_threshold: int = 25        # prag diferență pe pixel, 0..255
    min_active_ratio: float = 0.01   # proporția minimă de pixeli activi în ROI, 0..1
    max_gap_s: float = 0.5           # gol maxim între cadre active, în secunde
    morphology: bool = False         # curățare morfologică opțională

    def validate(self) -> None:
        if not 0 <= self.pixel_threshold <= 255:
            raise InvalidParameterError("Pragul pixelilor trebuie să fie între 0 și 255.")
        if not 0 <= self.min_active_ratio <= 1:
            raise InvalidParameterError("Aria minimă (proporție) trebuie să fie între 0 și 1.")
        if self.max_gap_s < 0:
            raise InvalidParameterError("Golul maxim nu poate fi negativ.")

    def to_dict(self) -> dict:
        return asdict(self)


def validate_video_path(path: str | Path) -> Path:
    p = Path(path)
    if not p.is_file():
        raise VideoFileError(f"Fișierul video nu există: {p}")
    return p