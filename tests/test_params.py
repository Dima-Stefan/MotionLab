import pytest

from motionlab.errors import InvalidParameterError, InvalidROIError, VideoFileError
from motionlab.params import ROI, DetectionParams, validate_video_path


def test_params_valizi():
    DetectionParams().validate()


def test_prag_negativ():
    with pytest.raises(InvalidParameterError):
        DetectionParams(pixel_threshold=-1).validate()


def test_prag_peste_255():
    with pytest.raises(InvalidParameterError):
        DetectionParams(pixel_threshold=300).validate()


def test_arie_in_afara_limitelor():
    with pytest.raises(InvalidParameterError):
        DetectionParams(min_active_ratio=1.5).validate()


def test_gol_negativ():
    with pytest.raises(InvalidParameterError):
        DetectionParams(max_gap_s=-1).validate()


def test_roi_in_afara_cadrului():
    with pytest.raises(InvalidROIError):
        ROI(600, 0, 100, 100).validate(640, 480)


def test_roi_valid():
    ROI(10, 10, 100, 100).validate(640, 480)


def test_fisier_lipsa():
    with pytest.raises(VideoFileError):
        validate_video_path("nu_exista.mp4")