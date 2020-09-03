from unittest.mock import Mock
from transformer.max_level_filter import MaxLevelFilter


def test_filter():
    level = 3
    m = MaxLevelFilter(level)
    record_pass = Mock(levelno=2)
    record_stop = Mock(levelno=level)
    assert m.filter(record_pass)
    assert not m.filter(record_stop)
