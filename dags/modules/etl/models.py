from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from database import Base
from datetime import datetime


class FactSales(Base):
    __tablename__ = "fact_sales"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_no = Column(String(20), nullable=False)
    stock_code = Column(String(20), ForeignKey("dim_product.stock_code"), nullable=False)
    customer_id = Column(String(20), nullable=True)
    invoice_date = Column(DateTime, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    country = Column(String(20), nullable=False)
    create_date = Column(DateTime, nullable=False, default=datetime.utcnow)

class DimProduct(Base):
    __tablename__ = "dim_product"

    stock_code = Column(String(20), primary_key=True)
    description = Column(String, nullable=True)

class OverviewIndex(Base):
    __tablename__ = "overview_index_etl"
    
    unique_customers = Column(Integer, primary_key=True)
    unique_transactions = Column(Integer, nullable=False)
    success_transaction = Column(Integer, nullable=False)
    cancel_transaction = Column(Integer, nullable=False)
    revenue = Column(Float, nullable=False)
    avg_revenue_per_transaction = Column(Float, nullable=False)
    avg_revenue_per_customer = Column(Float, nullable=False)
    
class OverviewByMonths(Base):
    __tablename__ = "overview_by_months_etl"
    
    mon = Column(DateTime, primary_key=True)
    unique_transactions = Column(Integer, nullable=False)
    unique_customers = Column(Integer, nullable=False)
    revenue = Column(Float, nullable=False)
    
    
class OverviewRFM(Base):
    __tablename__ = "rfm_etl"

    customer_id = Column(String(20), primary_key=True)
    
    recency = Column(Integer, nullable=False)
    frequency = Column(Integer, nullable=False) 
    monetary = Column(Float, nullable=False)
    recency_score = Column(Integer, nullable=False)
    frequency_score = Column(Integer, nullable=False)
    monetary_score = Column(Integer, nullable=False)
    rfm_score = Column(String, nullable=False)
    segment = Column(String, nullable=False)
    
class OverviewSegment(Base):
    __tablename__ = "rfm_segment_percentage_etl"
    
    segment = Column(String, primary_key=True)
    percentage = Column(Float, nullable=False)
    