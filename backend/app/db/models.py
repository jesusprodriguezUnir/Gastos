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
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=True)

    account = relationship("Account", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
    invoice = relationship("Invoice", back_populates="transactions")

class InvoiceCategory(Base):
    __tablename__ = "invoice_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    icon = Column(String, nullable=True) # e.g., 'droplet', 'zap' (Lucide icon name)

    invoices = relationship("Invoice", back_populates="invoice_category")

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    vendor = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="EUR")
    description = Column(String)
    
    # Links
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True) # General expense category
    invoice_category_id = Column(Integer, ForeignKey("invoice_categories.id"), nullable=True) # Specific invoice type (Luz, Agua)
    
    file_path = Column(String, nullable=False)

    category = relationship("Category")
    invoice_category = relationship("InvoiceCategory", back_populates="invoices")
    transactions = relationship("Transaction", back_populates="invoice")

class ImportRule(Base):
    __tablename__ = "import_rules"

    id = Column(Integer, primary_key=True, index=True)
    pattern = Column(String, nullable=False) # Regex or simple string
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    category = relationship("Category", back_populates="rules")
