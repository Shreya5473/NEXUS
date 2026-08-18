from app.tools.finance_tools import calculate_growth_rate


def test_growth_rate_positive():
    result = calculate_growth_rate(previous_value=100, current_value=120)
    assert result == 20.0


def test_growth_rate_negative():
    result = calculate_growth_rate(previous_value=100, current_value=80)
    assert result == -20.0


def test_growth_rate_zero_previous_raises_error():
    try:
        calculate_growth_rate(previous_value=0, current_value=50)
        assert False, "should have raised an error"
    except ValueError:
        pass