from unittest.mock import Mock
from transformer.extractor import Extractor


def test_select_cols_by_number(features):
    e = Extractor()
    e.FEATURES = features
    e.select_cols([0, 1])
    assert features[0].selected
    assert features[1].selected
    e.select_cols([])
    assert not features[0].selected
    assert not features[1].selected


def test_select_cols_by_name(features):
    e = Extractor()
    e.FEATURES = features
    e.select_cols(['f1', 'f2'])
    assert features[0].selected
    assert features[1].selected
    e.select_cols([])
    assert not features[0].selected
    assert not features[1].selected


def test_extract(data):
    e = Extractor()
    e._is_match = Mock(return_value=True)
    e.extract(data)
    assert len(e.rows) == len(data)
    e._is_match.assert_called()


def test_get_header_row_single_row_feature(features):
    features[1].selected = True
    e = Extractor()
    e.FEATURES = features
    output = e.get_header_row()
    expected = ['c']
    assert output == expected
    assert len(output) == len(expected)


def test_get_header_row_multiple_row_feature(features):
    features[0].selected = True
    e = Extractor()
    e.FEATURES = features
    output = e.get_header_row()
    expected = ['a', 'b']
    assert output == expected
    assert len(output) == len(expected)


def test_get_selected_features(features):
    features[0].selected = True
    e = Extractor()
    e.FEATURES = features
    output = e.get_selected_features()
    assert output[0] == e.FEATURES[0]
    assert len(output) == 1


def test_create_table():
    e = Extractor()
    e.rows = [['a', 'b'], ['c', 'd']]
    e.get_header_row = Mock()
    e._create_new_row = Mock()
    table = e.create_table()
    e.get_header_row.assert_called_once()
    assert e._create_new_row.call_count == len(e.rows)
    assert isinstance(table, list)
    assert len(table) == len(e.rows) + 1  # Mind the header row
    assert table[0] == e.get_header_row()


def test_create_new_row():
    pass


def test_get_features_names(features):
    features[0].selected = True
    e = Extractor()
    e.FEATURES = features
    output = e.get_features_names()
    assert output == [features[0].name, features[1].name]
