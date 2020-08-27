from transformer.feature import Feature
from unittest.mock import Mock, patch


def test_modify_if_modifier_is_set():
    f = Feature('date', 0)
    f.modifier = Mock(modify=Mock())
    date = '12.08.2019'
    output = f.modify(date)
    f.modifier.modify.assert_called_with(date)
    assert isinstance(output, Mock)


def test_modify_if_modifier_is_not_set():
    f = Feature('date', 0)
    date = '12.08.2019'
    output = f.modify(date)
    assert output == (date,)


def test_split_datetime():
    datetime = '25.03.2019 09:47'
    f = Feature('date', 0)
    date, time = f._split_datetime(datetime)
    assert date == '25.03.2019'
    assert time == '09:47'


def test_extract_number():
    f = Feature('date', 0)
    field = 'TC:   0,26'
    output = f._extract_number(field)
    assert output == ('0,26',)


def test_extract_number_if_not_existing():
    f = Feature('date', 0)
    field = 'TNb: '
    output = f._extract_number(field)
    assert output == ('NA',)


def test_set_modifier():
    f = Feature('date', 0)
    f._set_modifier('split_datetime')
    assert f.modifier.function == f._split_datetime
    assert f.modifier.new_cols == ('date', 'time')
    f._set_modifier('extract_number')
    assert f.modifier.function == f._extract_number
    assert f.modifier.new_cols == ('date',)


def test_get_new_cols():
    f = Feature('date', 0)
    f.modifier = Mock(new_cols=('date', 'time'))
    assert f.get_new_cols() == ('date', 'time')


def test__lt__():
    f1 = Feature('date', 0)
    f2 = Feature('time', 1)
    f3 = Feature('TOC', 1)
    assert f1 < f2
    assert not f2 < f3
    assert not f2 < f1
