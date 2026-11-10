"""Generează cele 3 clipuri demo și intervalele de referință (în secunde).

Rulare (din rădăcina proiectului):  python data/generate_clips.py
Clipurile sunt deterministe (fără zgomot aleator) și codate MJPG în .avi.
"""
from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

OUT_DIR = Path(__file__).resolve().parent
WIDTH, HEIGHT = 320, 240
FPS = 25
DURATION_S = 15
N_FRAMES = FPS * DURATION_S

OBJ_SIZE = 30
OBJ_GRAY = 230
OBJ_Y = 105


def make_background() -> np.ndarray:
    """Fundal static (gradient orizontal + dreptunghiuri fixe), în tonuri de gri."""
    row = np.linspace(80, 120, WIDTH, dtype=np.uint8)
    bg = np.tile(row, (HEIGHT, 1))
    bg[20:60, 30:90] = 60
    bg[170:220, 200:290] = 140
    return bg


def to_bgr(gray: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)


def write_clip(path: Path, frames: list[np.ndarray]) -> None:
    writer = cv2.VideoWriter(
        str(path), cv2.VideoWriter_fourcc(*"MJPG"), FPS, (WIDTH, HEIGHT)
    )
    if not writer.isOpened():
        raise RuntimeError(f"Nu pot scrie clipul {path}")
    for f in frames:
        writer.write(to_bgr(f))
    writer.release()


def write_reference(path: Path, intervals: list[tuple[float, float]]) -> None:
    """CSV cu aceeași structură ca exportul: id, start, sfarsit, durata (secunde)."""
    lines = ["id,start,sfarsit,durata"]
    for i, (s, e) in enumerate(intervals, start=1):
        lines.append(f"{i},{s:.2f},{e:.2f},{e - s:.2f}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def clip_static() -> tuple[list[np.ndarray], list[tuple[float, float]]]:
    bg = make_background()
    return [bg.copy() for _ in range(N_FRAMES)], []


def clip_motion(
    start_s: float = 2.0, stop_s: float = 7.0, speed_px: int = 2, x0: int = 20
) -> tuple[list[np.ndarray], list[tuple[float, float]]]:
    """Pătrat care se mișcă între start_s și stop_s, apoi rămâne oprit."""
    f_start, f_stop = round(start_s * FPS), round(stop_s * FPS)
    bg = make_background()
    frames = []
    for f in range(N_FRAMES):
        steps = min(max(f - f_start, 0), f_stop - f_start)
        x = x0 + speed_px * steps
        frame = bg.copy()
        frame[OBJ_Y : OBJ_Y + OBJ_SIZE, x : x + OBJ_SIZE] = OBJ_GRAY
        frames.append(frame)
    # Referință manuală: intervalul în care obiectul se mișcă efectiv.
    return frames, [(f_start / FPS, f_stop / FPS)]


def clip_illumination(
    on_s: float = 5.0, off_s: float = 10.0, delta: int = 50
) -> tuple[list[np.ndarray], list[tuple[float, float]]]:
    """Fără mișcare reală; luminozitate globală +delta între on_s și off_s."""
    bg = make_background()
    brighter = np.clip(bg.astype(np.int16) + delta, 0, 255).astype(np.uint8)
    f_on, f_off = round(on_s * FPS), round(off_s * FPS)
    frames = [brighter.copy() if f_on <= f < f_off else bg.copy() for f in range(N_FRAMES)]
    # Nicio mișcare reală -> referință goală. Evenimentele detectate la on_s și
    # off_s sunt false pozitive și se documentează ca limită a metodei A.
    return frames, []


def main() -> None:
    clips = {
        "clip_fara_miscare": clip_static,
        "clip_miscare": clip_motion,
        "clip_iluminare": clip_illumination,
    }
    for name, build in clips.items():
        frames, reference = build()
        write_clip(OUT_DIR / f"{name}.avi", frames)
        write_reference(OUT_DIR / f"{name}_ref.csv", reference)
        print(f"{name}: {len(frames)} cadre, referințe: {reference}")


if __name__ == "__main__":
    main()
