import pytest
from transformer.measurement_extractor import MeasurementExtractor

def test_measurement_record_is_match(measurement_record):
    me = MeasurementExtractor()
    match = me._is_match(measurement_record)
    assert match == True

def test_summary_record_is_no_match(summary_record):
    me = MeasurementExtractor()
    match = me._is_match(summary_record)
    assert match == False
