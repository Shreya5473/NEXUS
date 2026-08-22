from app.db.database import SessionLocal
from app.models.sales_record import SalesRecord


def get_sales_record(period: str) -> SalesRecord:
    db = SessionLocal()
    record = db.query(SalesRecord).filter(SalesRecord.period == period).first()
    db.close()

    if not record:
        raise ValueError(f"No sales record found for period '{period}'")

    return record


def calculate_conversion_rate(period: str) -> float:
    """
    period: e.g. "2026-06"
    Looks up real leads/conversions for that period and calculates the rate.
    """
    record = get_sales_record(period)

    if record.leads == 0:
        raise ValueError("leads cannot be zero — conversion rate undefined")

    rate = (record.conversions / record.leads) * 100
    return round(rate, 2)


def compare_conversion_rates(previous_period: str, current_period: str) -> float:
    """
    previous_period / current_period: e.g. "2026-06", "2026-07"
    Calculates both periods' rates from real data, returns the difference.
    """
    previous_rate = calculate_conversion_rate(previous_period)
    current_rate = calculate_conversion_rate(current_period)

    return round(current_rate - previous_rate, 2)