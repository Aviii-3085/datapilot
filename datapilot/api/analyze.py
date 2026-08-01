from datapilot.core.loader import load_dataset
from datapilot.core.report import Report


def analyze(data):
    dataset = load_dataset(data)
    return Report(dataset)