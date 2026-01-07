from sqlalchemy.orm import Session
from app.db import models, schemas

def get_accounts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Account).offset(skip).limit(limit).all()

def create_account(db: Session, account: schemas.AccountCreate):
    db_account = models.Account(**account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def get_account_by_name(db: Session, name: str):
    return db.query(models.Account).filter(models.Account.name == name).first()
