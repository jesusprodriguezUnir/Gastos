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

class TransactionCreate(TransactionBase):
    raw_import_data: Optional[str] = None

class Transaction(TransactionBase):
    id: int
    account: Account
    category: Optional[Category] = None

    class Config:
        from_attributes = True
