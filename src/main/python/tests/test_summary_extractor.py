import pytest
from transformer.summary_extractor import SummaryExtractor

def test_measurement_record_is_no_match(measurement_record):
    se = SummaryExtractor()
    match = se._is_match(measurement_record)
    assert match == False

def test_summary_record_is_match(summary_record):
    se = SummaryExtractor()
    match = se._is_match(summary_record)
    assert match == True
