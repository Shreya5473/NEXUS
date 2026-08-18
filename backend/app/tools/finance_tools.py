"""
Finance tools — plain, deterministic functions.
The Finance Agent will call these to get real numbers, never calculate them itself.
"""

def calculate_growth_rate(previous_value: float, current_value: float) -> float:
    """
    Calculates percentage growth between two periods.

    Example: previous=100, current=120 -> 20.0 (meaning +20%)
    """
    if previous_value == 0:
        raise ValueError("previous_value cannot be zero — growth rate undefined")

    growth = ((current_value - previous_value) / previous_value) * 100
    return round(growth, 2)