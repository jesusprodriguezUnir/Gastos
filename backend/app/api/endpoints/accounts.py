from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.services import account_service
from app.db import schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Account])
def read_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    return account_service.get_accounts(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.Account)
def create_account(account: schemas.AccountCreate, db: Session = Depends(deps.get_db)):
    return account_service.create_account(db, account=account)
