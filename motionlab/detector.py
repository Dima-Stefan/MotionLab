"""Metoda A: diferență între cadre consecutive + prag + arie minimă."""
from __future__ import annotations

import numpy as np

ROI = tuple[int, int, int, int]  # (x, y, lățime, înălțime)


def difference_mask(
    prev: np.ndarray, curr: np.ndarray, roi: ROI, pixel_threshold: int
) -> np.ndarray:
    """A1: |curr - prev| în tonuri de gri, apoi prag -> mască binară."""
    raise NotImplementedError


def is_active(mask: np.ndarray, min_area: float) -> bool:
    """A2: True dacă aria activă din ROI >= aria minimă (independentă de prag)."""
    raise NotImplementedError
