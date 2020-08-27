from .feature import Feature
from .extractor import Extractor


class SummaryExtractor(Extractor):
    FEATURES = (
        Feature('date', 0, modifier='split_datetime'),
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
