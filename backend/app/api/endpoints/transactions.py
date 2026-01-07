from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.services import transaction_service
from app.db import schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Transaction])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    return transaction_service.get_transactions(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(deps.get_db)):
    return transaction_service.create_transaction(db, transaction=transaction)
