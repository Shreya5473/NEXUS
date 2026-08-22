from app.tools.sales_tools import calculate_conversion_rate, compare_conversion_rates


def test_conversion_rate_june():
    # Seeded: June leads = 10200, conversions = 1120
    result = calculate_conversion_rate("2026-06")
    assert result == 10.98


def test_conversion_rate_missing_period_raises_error():
    try:
        calculate_conversion_rate("2099-01")
        assert False, "should have raised an error"
    except ValueError:
        pass


def test_compare_conversion_rates_june_to_july():
    # June: 10.98%, July: 7.55%
    result = compare_conversion_rates("2026-06", "2026-07")
    assert result == -3.43