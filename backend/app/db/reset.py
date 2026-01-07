from app.db.session import engine
from app.db.base import Base
from app.db.seed import seed_db

def reset_db():
    print("Resetting database...")
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    
    print("Re-creating tables...")
    Base.metadata.create_all(bind=engine)
    
    print("Database schema reset.")
    
    # Re-seed
    seed_db()
    print("Reset complete.")

if __name__ == "__main__":
    reset_db()
