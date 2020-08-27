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

    def create_table(self):
        table = [self.get_header_row()]
        for row in self.rows:
            newrow = []
            for feature in self.get_selected_features():
                field = row[feature.col]
                modified = feature.modify(field)
                for new_field in modified:
                    newrow.append(new_field)
            table.append(newrow)
        return table

    def get_features_names(self):
        return [f.name for f in self.FEATURES]
