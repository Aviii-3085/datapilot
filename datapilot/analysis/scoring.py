"""
Deterministic scoring utilities for Datapilot.
"""

import math


DEFAULT_DEGRADATION_EXPONENT = 1.2


def degradation_score(
    degradation_percentage: float,
    exponent: float = DEFAULT_DEGRADATION_EXPONENT,
) -> float:
    """
    Convert a degradation percentage into a continuous 0-100 score.

    The score:
    - is 100 when degradation is 0%
    - reaches 0 when degradation is 100%
    - decreases monotonically as degradation increases
    - remains bounded between 0 and 100
    """

    if not math.isfinite(degradation_percentage):
        raise ValueError(
            "degradation_percentage must be finite."
        )

    if not math.isfinite(exponent) or exponent <= 0:
        raise ValueError(
            "exponent must be greater than 0."
        )

    degradation = max(
        0.0,
        min(
            100.0,
            degradation_percentage,
        ),
    ) / 100.0

    score = (
        100.0
        * ((1.0 - degradation) ** exponent)
    )

    return round(
        max(0.0, min(100.0, score)),
        2,
    )
