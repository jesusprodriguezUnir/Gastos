from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    bank_name = Column(String, nullable=False) # 'CAIXA', 'ING', 'SABADELL', 'REVOLUT'
    currency = Column(String, default="EUR")

    transactions = relationship("Transaction", back_populates="account")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    type = Column(String) # 'INCOME', 'EXPENSE'
    parent_category = Column(String, nullable=True)

    transactions = relationship("Transaction", back_populates="category")
    rules = relationship("ImportRule", back_populates="category")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String)
    subcategory = Column(String, nullable=True)
    raw_import_data = Column(Text, nullable=True)
    
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    account = relationship("Account", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")

class ImportRule(Base):
    __tablename__ = "import_rules"

    id = Column(Integer, primary_key=True, index=True)
    pattern = Column(String, nullable=False) # Regex or simple string
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    category = relationship("Category", back_populates="rules")
