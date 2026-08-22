from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import Base


class SalesRecord(Base):
    __tablename__ = "sales_records"

    id = Column(Integer, primary_key=True)
    period = Column(String, nullable=False) 
    leads = Column(Integer, nullable=False)
    conversions = Column(Integer, nullable=False)