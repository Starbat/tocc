from transformer.modifier_factory import ModifierFactory


def test_split_datetime():
    mf = ModifierFactory.get_instance()
    datetime = '25.03.2019 09:47'
    date, time = mf._split_datetime(datetime)
    assert date == '25.03.2019'
    assert time == '09:47'


def test_extract_number():
    mf = ModifierFactory.get_instance()
    field = 'TC:   0,26'
    output = mf._extract_number(field)
    assert output == ('0,26',)


def test_extract_number_if_not_existing():
    mf = ModifierFactory.get_instance()
    field = 'TNb: '
    output = mf._extract_number(field)
    assert output == ('NA',)


def test_get_modifier():
    mf = ModifierFactory.get_instance()

    split_datetime_modifier = mf.get_modifier('split_datetime', 'X')
    assert split_datetime_modifier.function == mf._split_datetime
    assert split_datetime_modifier.new_cols == ('date', 'time')

    new_col_name = 'number'
    extract_number_modifier = mf.get_modifier('extract_number', new_col_name)
    assert extract_number_modifier.function == mf._extract_number
    assert extract_number_modifier.new_cols == (new_col_name,)

    new_col_name = 'column'
    identity_modifier = mf.get_modifier('', new_col_name)
    assert identity_modifier.function == mf._identity
    assert identity_modifier.new_cols == (new_col_name,)


def test_identity():
    mf = ModifierFactory.get_instance()
    test_data = (-1, 0, 1, -0.1, 0.1, '', 'string', ['a', 'b'])
    for d in test_data:
        assert mf._identity(d) == (d,)
