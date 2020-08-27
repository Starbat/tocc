#!/usr/bin/env python3
# This script reads a data table, transforms it and saves the results into a
# new file.
#
# Only rows beginning with a date are filtered; TNb column is removed;
# TIC, TC, TOC columns are cleared of text; header row is added;
# date and time are put into different columns.
#
# In the name of the new file, the suffix is replaced by '_filtered.csv'. It is
# saved to the same directory as the source file.
#
# Arguments:
# 1. arg: name or path of the file to process
#
# author: Till Schröder
# last edit: 25.08.2020

import csv
import sys
import os
import re
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

    def run(self):
        if len(self.extractors) == 0:
            sys.stderr.write('It must be determined which data should be ' +
                             'extracted!\n')
            sys.exit(1)
        print(f'input file: {self.input_file}')
        print(f'output directory: {self.output_dir}')
    #    self.check_paths()
        data = self.read_data()
        for extractor in self.extractors:
            extractor.extract(data=data)
            table = extractor.create_table()
            file = self.output_template.substitute(extraction=extractor.NAME)
            self.write_table(table, file)
        print('successfully completed')

    def read_data(self):
        print('Reading input file.')
        try:
            with open(self.input_file, mode='r', encoding='cp1252') as in_csv:
                csv_reader = csv.reader(in_csv, delimiter=';')
                return [row for row in csv_reader if row]  # skip emptry rows
        except FileNotFoundError:
            sys.stderr.write('A valid input file must be specified!\n')
            sys.exit(1)

    def write_table(self, table, file):
        print(file)
        print(f'Writing output file:\n{file}')
        if os.path.isfile(file):
            sys.stderr.write('Output file already exists! Delete, move or '
                             'rename existing file.\n')
            sys.exit(1)
        with open(file, mode='w', encoding='utf-8', newline='') as out_csv:
            csv_writer = csv.writer(out_csv, delimiter=';')
            for row in table:
                csv_writer.writerow(row)

    def basename_excl_extension(self, path):
        return re.match(self.BASENAME_REGEX, path)[2]

    # def format(self):
    #     # remove "TNb:" column
    #     del row[8]
    #     # put date and time in two columns
    #     date_time = row.pop(0).split()
    #     row.insert(0, date_time[1])
    #     row.insert(0, date_time[0])
    #     # remove text from "TIC:", "TC:", "TOC:" columns
    #     for i in range(6,9):
    #         row[i] = self._extract_number(row[i])
