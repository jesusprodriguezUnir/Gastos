from app.db.session import SessionLocal, engine
from app.db import models
from app.db.base import Base

def seed_db():
    print("Seeding database...")
    db = SessionLocal()
    
    # Check if accounts exist
    if db.query(models.Account).count() == 0:
        print("Creating default accounts...")
        accounts = [
            models.Account(name="Cuenta Principal", bank_name="CAIXA", currency="EUR"),
            models.Account(name="Ahorros", bank_name="ING", currency="EUR"),
            models.Account(name="Gastos Compartidos", bank_name="SABADELL", currency="EUR"),
            models.Account(name="Viajes", bank_name="REVOLUT", currency="EUR"),
        ]
        db.add_all(accounts)
        db.commit()
        print("Accounts created.")
    else:
        print("Accounts already exist.")

    # Check if categories exist
    if db.query(models.Category).count() == 0:
        print("Creating default categories...")
        categories = [
            models.Category(name="Supermercado", type="EXPENSE"),
            models.Category(name="Nómina", type="INCOME"),
            models.Category(name="Restaurantes", type="EXPENSE"),
            models.Category(name="Transporte", type="EXPENSE"),
            models.Category(name="Ocio", type="EXPENSE"),
            models.Category(name="Transferencias", type="EXPENSE"),
        ]
        db.add_all(categories)
        db.commit()
        print("Categories created.")
    else:
        print("Categories already exist.")

    # Check if invoice categories exist
    if db.query(models.InvoiceCategory).count() == 0:
        print("Creating default invoice categories...")
        inv_categories = [
            models.InvoiceCategory(name="Luz", icon="zap"),
            models.InvoiceCategory(name="Agua", icon="droplet"),
            models.InvoiceCategory(name="Gas", icon="flame"),
            models.InvoiceCategory(name="Internet/Teléfono", icon="wifi"),
            models.InvoiceCategory(name="Comunidad", icon="building"),
            models.InvoiceCategory(name="Nómina", icon="banknote"),
            models.InvoiceCategory(name="Seguros", icon="shield"),
            models.InvoiceCategory(name="Otros", icon="file-text"),
        ]
        db.add_all(inv_categories)
        db.commit()
        print("Invoice Categories created.")
    else:
        print("Invoice Categories already exist.")

    # Check if API keys exist
    if db.query(models.ApiKey).count() == 0:
        print("Creating default API key...")
        api_key = models.ApiKey(key="financeflow-api-key-2026", name="Default External API Key")
        db.add(api_key)
        db.commit()
        print("API Key created.")
    else:
        print("API Keys already exist.")

    db.close()
    print("Seeding complete.")

if __name__ == "__main__":
    seed_db()
