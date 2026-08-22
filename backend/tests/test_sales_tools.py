from app.tools.sales_tools import calculate_conversion_rate, compare_conversion_rates


def test_conversion_rate_normal():
    result = calculate_conversion_rate(leads=10200, conversions=1120)
    assert result == 10.98


def test_conversion_rate_zero_leads_raises_error():
    try:
        calculate_conversion_rate(leads=0, conversions=5)
        assert False, "should have raised an error"
    except ValueError:
        pass


def test_compare_conversion_rates_decline():
    result = compare_conversion_rates(previous_rate=10.9, current_rate=7.5)
    assert result == -3.4