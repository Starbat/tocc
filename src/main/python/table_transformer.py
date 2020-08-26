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


def get_extractors(summaries=False, measurements=False):
    extractors = []
    if summaries:
        extractors.append(SummaryExtractor())
    if measurements:
        extractors.append(MeasurementExtractor())
    for e in extractors:
        e.select_cols(e.get_features_names())
    return extractors

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


class Feature:
    DATE_REGEX = re.compile(r'\d{2}\.\d{2}\.\d{4}')
    FLOAT_REGEX = re.compile(r'\d+\,?\d*')

    def __init__(self, name: str, col: int, modifier='', selected=False):
        self.name = name
        self.col = col
        self._set_modifier(modifier)
        self.selected = selected

    def modify(self, string: str):
        return self.modifier(string) if self.modifier else string

    def _split_datetime(self, string):
        date, time = string.split()

    def _extract_number(self, string):
        number = re.search(self.FLOAT_REGEX, string)
        return number[0] if number else 'NA'

    def _set_modifier(self, name: str):
        if name == 'split_datetime':
            self.modifier = self._split_datetime
        elif name == 'extract_number':
            self.modifier = self._extract_number
        else:
            self.modifier = None

    def __lt__(self, other):
        return self.col < other.col


class Extractor:
    FEATURES = ()   # Override this
    NAME = ''       # and this.

    def __init__(self, *selected_cols, data=None):
        self.select_cols(selected_cols)
        if data:
            self.extract(data)

    def select_cols(self, selected):
        for feature in self.FEATURES:
            feature.selected = (feature.name in selected or
                                str(feature.col) in selected)

    def _is_match(self, row):
        """Override this identifier method!"""
        return False

    def extract(self, data):
        self.rows = [row for row in data if self._is_match(row)]

    def get_header_row(self):
        return [f.name for f in self.get_selected_features()]

    def get_selected_features(self):
        return [f for f in sorted(self.FEATURES) if f.selected]

    def create_table(self):
        table = [self.get_header_row()]
        for row in self.rows:
            newrow = []
            for feature in self.get_selected_features():
                field = row[feature.col]
                modified = feature.modify(field)
                newrow.append(modified)
            table.append(newrow)
        return table

    def get_features_names(self):
        return [f.name for f in self.FEATURES]


class SummaryExtractor(Extractor):
    FEATURES = (
        Feature('date', 0),
        Feature('No', 1),
        Feature('sample', 2),
        Feature('method', 3),
        Feature('n', 4),
        Feature('TIC', 5, modifier='extract_number'),
        Feature('TC', 6, modifier='extract_number'),
        Feature('TOC', 7, modifier='extract_number'),
        Feature('TNb', 8, modifier='extract_number'),
        Feature('comment', 9),
    )
    NAME = 'summaries'

    def __init__(self, *selected_cols, data=None):
        super().__init__(*selected_cols, data=data)

    def _is_match(self, row):
        return len(row) == 10


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


class MeasurementExtractor(Extractor):
    FEATURES = (
        Feature('sample', 0),
        Feature('TIC', 1),
        Feature('TC', 2),
        Feature('X', 3),
        Feature('TIC_integral', 4),
        Feature('TC_integral', 5),
        Feature('X_integral', 6),
        Feature('datetime', 7),
    )
    NAME = 'measurements'

    def __init__(self, *selected_cols, data=None):
        super().__init__(*selected_cols, data=data)

    def _is_match(self, row):
        return len(row) == 8
