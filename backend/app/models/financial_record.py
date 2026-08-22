from sqlalchemy import Column, Integer, String, Float, Date
from app.db.database import Base


class FinancialRecord(Base):
    __tablename__ = "financial_records"

    id = Column(Integer, primary_key=True)
    period = Column(String, nullable=False)
    revenue = Column(Float, nullable=False)
    expenses = Column(Float, nullable=False)