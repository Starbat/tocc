from .measurement_extractor import MeasurementExtractor
from .summary_extractor import SummaryExtractor


def get_extractors(summaries=False, measurements=False):
    extractors = []
    if summaries:
        extractors.append(SummaryExtractor())
    if measurements:
        extractors.append(MeasurementExtractor())
    for e in extractors:
        e.select_cols(e.get_features_names())
    return extractors
