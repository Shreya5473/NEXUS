from app.db.database import SessionLocal
from app.models.financial_record import FinancialRecord
from app.models.sales_record import SalesRecord

db = SessionLocal()

# Clear existing data first, so re-running this script doesn't duplicate rows
db.query(FinancialRecord).delete()
db.query(SalesRecord).delete()

financial_data = [
    FinancialRecord(period="2026-Q1", revenue=1_150_000, expenses=800_000),
    FinancialRecord(period="2026-Q2", revenue=1_200_000, expenses=820_000),
    FinancialRecord(period="2026-Q3", revenue=1_344_000, expenses=975_000),
]

sales_data = [
    SalesRecord(period="2026-05", leads=10500, conversions=1180),
    SalesRecord(period="2026-06", leads=10200, conversions=1120),
    SalesRecord(period="2026-07", leads=9800, conversions=740),
]

db.add_all(financial_data)
db.add_all(sales_data)
db.commit()

print(f"Seeded {len(financial_data)} financial records and {len(sales_data)} sales records.")

db.close()