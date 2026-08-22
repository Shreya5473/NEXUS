from app.db.database import SessionLocal
from app.models.financial_record import FinancialRecord


def get_financial_record(period: str) -> FinancialRecord:
    db = SessionLocal()
    record = db.query(FinancialRecord).filter(FinancialRecord.period == period).first()
    db.close()

    if not record:
        raise ValueError(f"No financial record found for period '{period}'")

    return record


def calculate_growth_rate(previous_period: str, current_period: str) -> float:
    """
    previous_period / current_period: e.g. "2026-Q1", "2026-Q2"
    Looks up real revenue for both periods and calculates percentage growth.
    """
    previous = get_financial_record(previous_period)
    current = get_financial_record(current_period)

    if previous.revenue == 0:
        raise ValueError("previous period revenue cannot be zero — growth rate undefined")

    growth = ((current.revenue - previous.revenue) / previous.revenue) * 100
    return round(growth, 2)