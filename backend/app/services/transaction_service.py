from sqlalchemy.orm import Session
from app.db import models, schemas
from typing import List

def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Transaction).offset(skip).limit(limit).all()

def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def create_transactions_bulk(db: Session, transactions: List[schemas.TransactionCreate]):
    db_transactions = [models.Transaction(**t.dict()) for t in transactions]
    db.add_all(db_transactions)
    db.commit()
    # Refreshing all might be slow, usually just return success or IDs
    return db_transactions
