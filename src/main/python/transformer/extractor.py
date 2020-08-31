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
                                feature.col in selected)

    def _is_match(self, row):
        """Override this identifier method!"""
        return False

    def extract(self, data):
        self.rows = [row for row in data if self._is_match(row)]

    def get_header_row(self):
        header_row = []
        for feature in self.get_selected_features():
            for col in feature.get_new_cols():
                header_row.append(col)
        return header_row

    def get_selected_features(self):
        return [f for f in sorted(self.FEATURES) if f.selected]

    def create_table(self) -> list:
        table = [self.get_header_row()]
        for row in self.rows:
            newrow = self._create_new_row(row)
            table.append(newrow)
        return table

    def _create_new_row(self, row: list) -> list:
        newrow = []
        for feature in self.get_selected_features():
            newfields = feature.modify(row[feature.col])
            for field in newfields:
                newrow.append(field)
        return newrow

    def get_features_names(self):
        return [f.name for f in self.FEATURES]
