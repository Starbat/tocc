from .feature import Feature
from .extractor import Extractor


class MeasurementExtractor(Extractor):
    FEATURES = (
        Feature('sample', 0),
        Feature('TIC', 1),
        Feature('TC', 2),
        Feature('X', 3),
        Feature('TIC_integral', 4),
        Feature('TC_integral', 5),
        Feature('X_integral', 6),
        Feature('time', 7, modifier='split_datetime'),
    )
    NAME = 'measurements'

    def __init__(self, *selected_cols, data=None):
        super().__init__(*selected_cols, data=data)

    def _is_match(self, row):
        return len(row) == 8
