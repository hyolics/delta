from sqlalchemy import Column, String, Integer, Float, DateTime
from datetime import datetime
from modules.database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_no = Column(String(20), nullable=False)
    stock_code = Column(String(20), nullable=False)
    description = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    invoice_date = Column(DateTime, nullable=False)
    unit_price = Column(Float, nullable=False)
    customer_id = Column(String(20), nullable=True)
    country = Column(String, nullable=False)
    create_date = Column(DateTime, nullable=False, default=datetime.utcnow)
