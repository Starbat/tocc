import pytest
from unittest.mock import Mock, PropertyMock


@pytest.fixture
def features():
    lt = lambda x, y: x.col < y.col
    duplicate = lambda x: (x, x)
    identity = lambda x: x
    f1 = Mock(col=0, modify=duplicate, selected=False)
    type(f1).name = PropertyMock(return_value='f1')
    f1.__lt__ = lt
    f1.get_new_cols = Mock(return_value=['a', 'b'])

    f2 = Mock(col=1, modify=identity, selected=False)
    type(f2).name = PropertyMock(return_value='f2')
    f2.__lt__ = lt
    f2.get_new_cols = Mock(return_value=['c'])
    return (f1, f2)


@pytest.fixture
def data_record():
    return ['x', 'y']


@pytest.fixture
def measurement_record():
    record = ['dest. H2O pH2,0', '0,00000', '0,83807', '', '0', '116', '0',
              '25.03.2019 10:38']
    return record


@pytest.fixture
def summary_record():
    record = ['25.03.2019 09:47', '01', 'dest. H2O ', '31', '3', 'TIC:   0,12',
              'TC:   0,26', 'TOC:   0,00', 'TNb: ', 'nach Kalibrierg']
    return record


@pytest.fixture
def data(measurement_record, summary_record):
    return [measurement_record, summary_record]
