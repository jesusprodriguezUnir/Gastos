from sqlalchemy.orm import Session
from app.db import models, schemas
import re
from typing import List

class Categorizer:
    def __init__(self, db: Session):
        self.rules = db.query(models.ImportRule).all()

    def predict_category(self, description: str) -> int:
        """
        Returns category_id if a rule matches, else None.
        """
        if not description:
            return None
            
        for rule in self.rules:
            # Simple case-insensitive match for now, can be regex
            try:
                if re.search(rule.pattern, description, re.IGNORECASE):
                    return rule.category_id
            except re.error:
                continue
        return None

def apply_categorization(db: Session, transactions: List[schemas.TransactionCreate]) -> List[schemas.TransactionCreate]:
    categorizer = Categorizer(db)
    for t in transactions:
        if not t.category_id:
            t.category_id = categorizer.predict_category(t.description)
    return transactions
