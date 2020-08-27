import pytest
from transformer.summary_extractor import SummaryExtractor
from transformer.measurement_extractor import MeasurementExtractor
from transformer.helpers import get_extractors


def test_get_summary_extractor():
    output = get_extractors(summaries=True)
    assert type(output[0]) == SummaryExtractor
    assert len(output) == 1


def test_get_measurement_extractor():
    output = get_extractors(measurements=True)
    assert type(output[0]) == MeasurementExtractor
    assert len(output) == 1


def test_get_two_extractors():
    output = get_extractors(measurements=True, summaries=True)
    assert len(output) == 2
