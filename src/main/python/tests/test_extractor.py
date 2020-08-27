import pytest
from transformer.extractor import Extractor
from unittest.mock import patch


def test_select_cols_by_number(features):
    e = Extractor()
    e.FEATURES = features
    e.select_cols([0, 1])
    assert features[0].selected == True
    assert features[1].selected == True

def test_select_cols_by_name(features):
    e = Extractor()
    e.FEATURES = features
    e.select_cols(['f1', 'f2'])
    assert features[0].selected == True
    assert features[1].selected == True


def test_extract(data):
    e = Extractor()
    e.extract(data)
    assert len(e.rows) == 0
