from pydantic import BaseModel
from typing import Optional, List
from datetime import date

# Account Schemas
class AccountBase(BaseModel):
    name: str
    bank_name: str
    currency: str = "EUR"

class AccountCreate(AccountBase):
    pass

class Account(AccountBase):
    id: int

    class Config:
        from_attributes = True

# Category Schemas
class CategoryBase(BaseModel):
    name: str
    type: str  # INCOME, EXPENSE
    parent_category: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True

# Transaction Schemas
class TransactionBase(BaseModel):
    date: date
    amount: float
    description: Optional[str] = None
    subcategory: Optional[str] = None
    account_id: int
    category_id: Optional[int] = None
    invoice_id: Optional[int] = None

class TransactionCreate(TransactionBase):
    raw_import_data: Optional[str] = None

class Transaction(TransactionBase):
    id: int
    account: Account
    category: Optional[Category] = None

    class Config:
        from_attributes = True

# Invoice Category Schemas
class InvoiceCategoryBase(BaseModel):
    name: str
    icon: Optional[str] = None

class InvoiceCategoryCreate(InvoiceCategoryBase):
    pass

class InvoiceCategory(InvoiceCategoryBase):
    id: int
    class Config:
        from_attributes = True

# Invoice Schemas
class InvoiceBase(BaseModel):
    vendor: str
    date: date
    amount: float
    currency: str = "EUR"
    description: Optional[str] = None
    category_id: Optional[int] = None
    invoice_category_id: Optional[int] = None

class InvoiceCreate(InvoiceBase):
    pass

class Invoice(InvoiceBase):
    id: int
    file_path: str
    invoice_category: Optional[InvoiceCategory] = None

    class Config:
        from_attributes = True

# Update Transaction to include simple Invoice reference or id if needed
# Re-defining Transaction to update forward references if necessary

