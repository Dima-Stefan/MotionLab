"""Export: intervale -> CSV, parametri -> JSON."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from motionlab.intervals import Interval


def export_csv(intervals: list[Interval], path: Path) -> None:
    """Scrie intervale.csv cu coloanele: id, start, sfârșit, durată."""
    raise NotImplementedError


def export_json(params: dict[str, Any], path: Path) -> None:
    """Scrie parametri.json: ROI, prag, arie minimă, gol maxim."""
    raise NotImplementedError
