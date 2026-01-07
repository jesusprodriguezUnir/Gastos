from typing import Generator
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db import models

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_api_key(x_api_key: str = Header(..., alias="X-API-Key"), db: Session = Depends(get_db)):
    api_key = db.query(models.ApiKey).filter(models.ApiKey.key == x_api_key, models.ApiKey.is_active == True).first()
    if not api_key:
        raise HTTPException(status_code=401, detail="Invalid or inactive API key")
    return api_key
