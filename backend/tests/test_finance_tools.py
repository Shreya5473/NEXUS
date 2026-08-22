from app.tools.finance_tools import calculate_growth_rate


def test_growth_rate_q2_to_q3():
    # Seeded: Q2 revenue = 1,200,000, Q3 revenue = 1,344,000
    result = calculate_growth_rate("2026-Q2", "2026-Q3")
    assert result == 12.0


def test_growth_rate_missing_period_raises_error():
    try:
        calculate_growth_rate("2026-Q2", "2099-Q1")
        assert False, "should have raised an error"
    except ValueError:
        pass