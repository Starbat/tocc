import re
from .modifier import Modifier

class Feature:
    DATE_REGEX = re.compile(r'\d{2}\.\d{2}\.\d{4}')
    FLOAT_REGEX = re.compile(r'\d+\,?\d*')

    def __init__(self, name: str, col: int, modifier='', selected=False):
        self.name = name
        self.col = col
        self._set_modifier(modifier)
        self.selected = selected

    def modify(self, string: str):
        return self.modifier.modify(string)

    def _split_datetime(self, string: str) -> list:
        return string.split()

    def _extract_number(self, string: str) -> list:
        number = re.search(self.FLOAT_REGEX, string)
        return (number[0],) if number else ('NA',)

    def _set_modifier(self, name: str):
        if name == 'split_datetime':
            self.modifier = Modifier(self._split_datetime, 'date', 'time')
        elif name == 'extract_number':
            self.modifier = Modifier(self._extract_number, self.name)
        else:
            self.modifier = Modifier(lambda x: (x,), self.name)

    def get_new_cols(self):
        return self.modifier.new_cols

    def __lt__(self, other):
        return self.col < other.col
