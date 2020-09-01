import csv
import os
import re
from logging import getLogger, INFO
from string import Template


class TableTransformer:
    BASENAME_REGEX = re.compile(r'(.*\/)?(.+)\..+$')

    def __init__(self, file_name, *extractors, output_dir=None):
        self.input_file = os.path.abspath(file_name)
        self.base_name = self.basename_excl_extension(self.input_file)
        self.extractors = extractors
        if output_dir:
            self.output_dir = output_dir
        else:
            self.output_dir = os.path.dirname(self.input_file)
        self.output_template = Template(os.path.join(self.output_dir,
                                                     self.base_name) +
                                        '_${extraction}.csv')
        self.logger = self._create_logger()

    def _create_logger(self):
        logger = getLogger(__name__)
        logger.setLevel(INFO)
        return logger

    def run(self):
        if len(self.extractors) > 0:
            self.logger.info(f'Input file: {self.input_file}')
            self.logger.info(f'Output directory: {self.output_dir}')

            data = self.read_data()
            if data:
                for extractor in self.extractors:
                    extractor.extract(data=data)
                    table = extractor.create_table()
                    file = self.output_template.substitute(
                                                    extraction=extractor.NAME)
                    try:
                        self.write_table(table, file)
                    except FileExistsError as e:
                        self.logger.error(e.args[0])
        else:
            self.logger.error('It must be determined which data should be ' +
                              'extracted!')

    def read_data(self):
        try:
            with open(self.input_file, mode='r', encoding='cp1252') as file:
                csv_reader = csv.reader(file, delimiter=';')
                return [row for row in csv_reader if row]  # skip emptry rows
        except FileNotFoundError:
            self.logger.error(f'Input file does not exist: {self.base_name}')
            return None
        except IsADirectoryError:
            self.logger.error('A directory is not a valid input file!')
            return None

    def write_table(self, table, file):
        if os.path.isfile(file):
            raise FileExistsError('Output file already exists: ',
                                  os.path.basename(file))
        with open(file, mode='w', encoding='utf-8', newline='') as out_csv:
            self.logger.info(f'Writing output file: {os.path.basename(file)}')
            csv_writer = csv.writer(out_csv, delimiter=';')
            for row in table:
                csv_writer.writerow(row)

    def basename_excl_extension(self, path):
        match = re.match(self.BASENAME_REGEX, path)
        if match:
            return match[2]
        else:
            return ''
