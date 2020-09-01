import re
from .modifier import Modifier


class ModifierFactory:
    _instance = None
    FLOAT_REGEX = re.compile(r'\d+\,?\d*')

    def __init__(self):
        if ModifierFactory._instance:
            raise Exception('The constructor of this singleton was called ' +
                            'repeatedly.')
        else:
            ModifierFactory._instance = self

    @staticmethod
    def get_instance():
        if not ModifierFactory._instance:
            ModifierFactory()
        return ModifierFactory._instance

    def get_modifier(self, name: str, new_col_name: str) -> Modifier:
        if name == 'split_datetime':
            return Modifier(self._split_datetime, 'date', 'time')
        elif name == 'extract_number':
            return Modifier(self._extract_number, new_col_name)
        else:
            return Modifier(self._identity, new_col_name)

    def _split_datetime(self, string: str) -> tuple:
        return string.split()

    def _extract_number(self, string: str) -> tuple:
        number = re.search(self.FLOAT_REGEX, string)
        return (number[0],) if number else ('NA',)

    def _identity(self, x):
        return (x,)
