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
# last edit: 21.08.2020

import csv
import sys
import os
import re

class TableTransformer:
    HEADER = ['date', 'time', 'No', 'sample', 'method', 'n', 'DIC', 'DC',
              'DOC', 'comment']
    DATE_REGEX = re.compile('\d{2}\.\d{2}\.\d{4}')
    FLOAT_REGEX = re.compile('\d+\,?\d*')
    BASENAME_REGEX = re.compile('(.+)\..+$')

    def __init__(self, file_name, output_path=None):
        self.input_path = os.path.abspath(file_name)
        if not output_path:
            self.output_path = self.basename_excl_extension(self.input_path) \
                                + '_filtered.csv'
        else:
            self.output_path = output_path

    def main(self):
        print(f'input file: {self.input_path}')
        print(f'output file: {self.output_path}')
        self.check_paths()
        data = self.read_data()
        self.write_table(data)
        print('successfully completed')

    def read_data(self):
        print('reading input file')
        data = []
        with open(self.input_path, mode='r', encoding='cp1252') as in_csv:
            csv_reader = csv.reader(in_csv, delimiter=';')
            for row in csv_reader:
                if row and bool(re.match(self.DATE_REGEX, row[0])):
                    data.append(row)
        return data

    def write_table(self, data):
        print('writing output file')
        with open(self.output_path,
                  mode='w', encoding='cp1252', newline='') as out_csv:
            csv_writer = csv.writer(out_csv, delimiter=';')
            # write header line
            csv_writer.writerow(self.HEADER)
            for row in data:
                self.format_row(row)
                csv_writer.writerow(row)

    def check_paths(self):
        # Check if input file is a valid file. Otherwise stop.
        if not os.path.isfile(self.input_path):
            sys.stderr.write('A valid input file must be specified!\n')
            sys.exit(1)
        # Check if output file already exits and stop if it does.
        if os.path.isfile(self.output_path):
            sys.stderr.write('Output file already exists! Delete, move or '
                             'rename existing file.\n')
            sys.exit(1)

    def format_row(self, row):
        # remove "TNb:" column
        del row[8]
        # put date and time in two columns
        date_time = row.pop(0).split()
        row.insert(0, date_time[1])
        row.insert(0, date_time[0])
        # remove text from "TIC:", "TC:", "TOC:" columns
        for i in range(6,9):
            row[i] = self.extract_number(row[i])

    def extract_number(self, string):
        number = re.search(self.FLOAT_REGEX, string)
        if number:
            return number[0]
        else:
            return 'NA'

    def basename_excl_extension(self, path):
        return re.findall(self.BASENAME_REGEX, path)[0]
