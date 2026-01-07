from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.services import category_service
from app.db import schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    return category_service.get_categories(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(deps.get_db)):
    return category_service.create_category(db, category=category)
