def calculate_conversion_rate(leads: int, conversions: int) -> float:
    """
    leads=10200, conversions=1120 -> 10.98 (meaning 10.98%)
    """
    if leads == 0:
        raise ValueError("leads cannot be zero — conversion rate undefined")

    rate = (conversions / leads) * 100
    return round(rate, 2)


def compare_conversion_rates(previous_rate: float, current_rate: float) -> float:
    """
    Difference in percentage points between two conversion rates.
    previous_rate=10.9, current_rate=7.5 -> -3.4
    """
    return round(current_rate - previous_rate, 2)