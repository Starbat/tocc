from .modifier_factory import ModifierFactory


class Feature:
    def __init__(self, name: str, col: int, modifier='', selected=False):
        self.name = name
        self.col = col
        self.modifier = self._get_modifier(modifier, name)
        self.selected = selected

    def modify(self, string: str):
        return self.modifier.modify(string)

    def _get_modifier(self, name: str, new_col_name):
        mf = ModifierFactory.get_instance()
        return mf.get_modifier(name, new_col_name)

    def get_new_cols(self):
        return self.modifier.new_cols

    def __lt__(self, other):
        return self.col < other.col
