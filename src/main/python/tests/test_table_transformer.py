import pytest
from unittest.mock import Mock, patch
from transformer.table_transformer import TableTransformer


def test_run():
    tt = TableTransformer('file.txt')
    tt.extractors = [Mock(), Mock()]
    tt.logger = Mock()
    tt.read_data = Mock()
    tt.write_table = Mock()
    tt.output_template = Mock()
    tt.run()

    for e in tt.extractors:
        e.extract.assert_called_once()
        e.create_table.assert_called_once()
    tt.read_data.assert_called_once()
    assert len(tt.write_table.call_args_list) == len(tt.extractors)
    assert (len(tt.output_template.substitute.call_args_list)
            == len(tt.extractors))


def test_run_does_nothing_if_no_data():
    tt = TableTransformer('file.txt')
    tt.extractors = [Mock(), Mock()]
    tt.read_data = Mock(return_value=None)
    tt.write_table = Mock()
    tt.run()

    tt.read_data.assert_called()
    tt.write_table.assert_not_called()
    for e in tt.extractors:
        e.extract.assert_not_called()
        e.create_table.assert_not_called()

def test_run_does_nothing_if_no_extractor():
    tt = TableTransformer('file.txt')
    tt.extractors = []
    tt.logger = Mock()
    tt.read_data = Mock()
    tt.write_table = Mock()
    tt.run()

    tt.read_data.assert_not_called()
    tt.write_table.assert_not_called()
    tt.logger.error.assert_called()


def test_run_catches_FileExistsError():
    tt = TableTransformer('file.txt')
    tt.extractors = [Mock(), Mock()]
    tt.logger = Mock()
    tt.read_data = Mock()
    tt.write_table = Mock(side_effect=FileExistsError('error'))
    tt.run()

    assert len(tt.logger.error.call_args_list) == len(tt.extractors)


@patch('transformer.table_transformer.open')
@patch('transformer.table_transformer.csv.reader')
def test_read_data(mock_csv_reader, mock_open, data):
    mock_csv_reader.return_value = data
    tt = TableTransformer('file.txt')
    output = tt.read_data()

    mock_open.assert_called()
    mock_csv_reader.assert_called()
    assert output == data


@patch('transformer.table_transformer.open')
def test_read_data_file_not_found(mock_open):
    mock_open.side_effect = FileNotFoundError()
    tt = TableTransformer('file.txt')
    tt.logger = Mock()
    output = tt.read_data()

    mock_open.assert_called()
    tt.logger.error.assert_called()
    assert output is None


@patch('transformer.table_transformer.open')
def test_read_data_path_is_dir(mock_open):
    mock_open.side_effect = IsADirectoryError()
    tt = TableTransformer('file.txt')
    tt.logger = Mock()
    output = tt.read_data()

    mock_open.assert_called()
    tt.logger.error.assert_called()
    assert output is None


@patch('transformer.table_transformer.open')
@patch('transformer.table_transformer.csv.writer')
def test_write_table(mock_csv_writer, mock_open, data):
    csv_writer_instance = Mock()
    mock_csv_writer.return_value = csv_writer_instance
    file = 'file.txt'
    tt = TableTransformer('file.txt')
    tt.write_table(data, file)

    mock_open.assert_called_with(file, mode='w', encoding='utf-8', newline='')
    mock_csv_writer.assert_called()
    assert len(csv_writer_instance.writerow.call_args_list) == 2
    csv_writer_instance.writerow.assert_called_with(data[1])


@patch('transformer.table_transformer.open')
@patch('transformer.table_transformer.os.path.isfile')
def test_write_table_does_not_overwrite(mock_is_file, mock_open):
    mock_is_file.return_value = True
    tt = TableTransformer('file.txt')

    with pytest.raises(FileExistsError):
        tt.write_table('table', 'file')
    mock_open.assert_not_called()


def test_basename_excl_extension():
    tt = TableTransformer('file.txt')
    path = '/path/to/basename.txt'
    output = tt.basename_excl_extension(path)
    assert output == 'basename'

    path = 'basename.txt'
    output = tt.basename_excl_extension(path)
    assert output == 'basename'

    path = 'nonsense'
    output = tt.basename_excl_extension(path)
    assert output == ''
