import sqlite3
import os

DB_PATH = "finance.db"

def migrate():
    print(f"Connecting to database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 1. Create invoices table
        print("Creating invoices table...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor VARCHAR NOT NULL,
            date DATE NOT NULL,
            amount FLOAT NOT NULL,
            currency VARCHAR DEFAULT 'EUR',
            description VARCHAR,
            category_id INTEGER,
            file_path VARCHAR NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
        """)

        # 2. Add invoice_id to transactions table
        print("Checking if invoice_id column exists in transactions...")
        cursor.execute("PRAGMA table_info(transactions)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if "invoice_id" not in columns:
            print("Adding invoice_id column to transactions...")
            cursor.execute("ALTER TABLE transactions ADD COLUMN invoice_id INTEGER REFERENCES invoices(id)")
        else:
            print("invoice_id column already exists.")

        conn.commit()
        print("Migration completed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        # Allow running from backend directory
        if os.path.exists(os.path.join("backend", DB_PATH)):
            DB_PATH = os.path.join("backend", DB_PATH)
        elif os.path.exists(os.path.join("..", DB_PATH)):
             DB_PATH = os.path.join("..", DB_PATH)
             
    migrate()
