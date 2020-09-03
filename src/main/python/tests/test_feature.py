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


@patch('transformer.feature.ModifierFactory.get_instance')
def test_get_modifier(mock_get_instance):
    modifier_factory = Mock()
    mock_get_instance.return_value = modifier_factory
    f = Feature('date', 0)

    name = 'test name'
    new_col_name = 'test_col_name'
    output = f._get_modifier(name, new_col_name)
    mock_get_instance.assert_called()
    modifier_factory.get_modifier.assert_called_with(name, new_col_name)
    assert output


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
