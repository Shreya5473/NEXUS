from app.db.database import Base, engine
from app.models.financial_record import FinancialRecord
from app.models.sales_record import SalesRecord

Base.metadata.create_all(bind=engine)
print("Tables created successfully.")