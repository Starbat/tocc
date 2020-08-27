from transformer.table_transformer import TableTransformer


def test_basename_excl_extension():
    tt = TableTransformer('file.txt')
    path = '/path/to/basename.txt'
    output = tt.basename_excl_extension(path)
    assert output == 'basename'
