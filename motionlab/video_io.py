"""Citire video și timpul fiecărui cadru."""
from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import numpy as np


def get_fps(path: Path) -> float:
    """Returnează FPS-ul clipului."""
    raise NotImplementedError


def read_frames(path: Path) -> Iterator[tuple[int, float, np.ndarray]]:
    """Generează (index_cadru, timp_în_secunde, cadru_BGR)."""
    raise NotImplementedError
