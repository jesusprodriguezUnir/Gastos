from app.services import transaction_service
from app.db import schemas
from datetime import date

def test_create_transaction(db):
    t_data = schemas.TransactionCreate(
        date=date(2025, 1, 1),
        amount=100.0,
        description="Test Transaction",
        account_id=1
    )
    # We need an account first. But wait, seed is not run in test db automatically.
    # We must create an account in 'db' fixture or inside verify test.
    from app.db.models import Account
    acc = Account(name="TestAcc", bank_name="TEST", currency="EUR")
    db.add(acc)
    db.commit()
    db.refresh(acc)

    t_data.account_id = acc.id
    
    created = transaction_service.create_transaction(db, t_data)
    assert created.id is not None
    assert created.amount == 100.0
    assert created.account_id == acc.id

def test_categorizer(db):
    from app.services.categorizer import apply_categorization
    from app.db.models import Category, ImportRule
    from app.db import models

    # Setup Categories & Rules
    cat = Category(name="Food", type="EXPENSE")
    db.add(cat)
    db.commit()
    
    rule = ImportRule(pattern="Mercadona", category_id=cat.id)
    db.add(rule)
    db.commit()

    # Create dummy transactions
    t1 = schemas.TransactionCreate(
        date=date(2025,1,1), amount=-50, description="COMPRA MERCADONA MADRID", account_id=1
    )
    t2 = schemas.TransactionCreate(
        date=date(2025,1,1), amount=-20, description="GASOLINERA DESCONOCIDA", account_id=1
    )
    
    results = apply_categorization(db, [t1, t2])
    
    assert results[0].category_id == cat.id
    assert results[1].category_id is None
