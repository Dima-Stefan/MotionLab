"""Excepții specifice aplicației MotionLab."""


class MotionLabError(Exception):
    """Clasa de bază pentru toate erorile aplicației."""


class VideoFileError(MotionLabError):
    """Fișierul video lipsește sau nu poate fi deschis."""


class InvalidROIError(MotionLabError):
    """ROI invalid sau în afara cadrului."""


class InvalidParameterError(MotionLabError):
    """Parametru negativ, lipsă sau în afara limitelor."""


class ExportError(MotionLabError):
    """Eroare la scrierea fișierelor CSV/JSON."""