from fastapi import APIRouter
from app.api.endpoints import transactions, accounts, categories, upload

api_router = APIRouter()
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
