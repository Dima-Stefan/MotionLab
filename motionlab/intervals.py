"""Gruparea cadrelor active în intervale, cu gol maxim."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Interval:
    id: int
    start: float  # secunde
    end: float  # secunde

    @property
    def duration(self) -> float:
        return self.end - self.start


def group_intervals(active_times: list[float], max_gap: float) -> list[Interval]:
    """Grupează momentele active vecine; un gol > max_gap încheie intervalul."""
    raise NotImplementedError
