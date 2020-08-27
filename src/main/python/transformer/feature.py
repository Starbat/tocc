import re


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
