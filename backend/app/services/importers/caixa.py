from typing import List
from app.db.schemas import TransactionCreate
from app.services.importers.base import BaseImporter
import pandas as pd
from datetime import datetime

class CaixaImporter(BaseImporter):
    def parse(self, file_path: str, account_id: int) -> List[TransactionCreate]:
        print(f"Reading file: {file_path}")
        try:
            # Determine file type based on extension
            is_excel = file_path.endswith('.xlsx') or file_path.endswith('.xls')
            
            if is_excel:
                df_temp = pd.read_excel(file_path, header=None, nrows=10)
            else:
                df_temp = pd.read_csv(file_path, header=None, nrows=10)
                
            header_row_index = -1
            for i, row in df_temp.iterrows():
                row_values = [str(x).strip() for x in row.values]
                if 'Fecha' in row_values and 'Concepto' in row_values:
                    header_row_index = i
                    break
            
            if header_row_index == -1:
                print("Header row not found, trying default read...")
                df = self.read_file(file_path)
            else:
                print(f"Header found at row {header_row_index}")
                if is_excel:
                    df = pd.read_excel(file_path, header=header_row_index)
                else:
                    df = pd.read_csv(file_path, header=header_row_index)

            # Strip whitespace from column names
            df.columns = df.columns.str.strip()
            
            print(f"File loaded. Columns found: {list(df.columns)}")
            print(f"Total rows in file: {len(df)}")
        except Exception as e:
            print(f"Error reading file: {e}")
            raise e
            
        transactions = []
        for _, row in df.iterrows():
            # Adjust column names based on the screenshot provided
            # 'Fecha', 'Concepto', 'Categoría', 'Importe (€)', 'Tipo Movimiento', 'Cuenta/Tarjeta'
            
            # 1. Date
            date_val = row.get('Fecha')
            if pd.isna(date_val):
                continue # Skip empty rows
                
            try:
                if isinstance(date_val, datetime):
                    date_obj = date_val.date()
                else:
                    # Parse DD/MM/YYYY
                    date_str = str(date_val).split(" ")[0]
                    date_obj = datetime.strptime(date_str, '%d/%m/%Y').date()
            except Exception as e:
                print(f"Date parse error for {date_val}: {e}")
                date_obj = datetime.now().date()

            # 2. Amount
            # Look for 'Importe (€)' or just 'Importe'
            amount_col = next((c for c in df.columns if 'Importe' in c), 'Importe')
            amount_val = row.get(amount_col, 0.0)
            
            try:
                if isinstance(amount_val, (int, float)) and not pd.isna(amount_val):
                    amount = float(amount_val)
                else:
                    # Parse string: "1.200,50" -> 1200.50
                    val_str = str(amount_val).replace('€', '').strip()
                    if ',' in val_str and '.' in val_str:
                         # Assume 1.000,00 format
                         val_str = val_str.replace('.', '').replace(',', '.')
                    elif ',' in val_str:
                        # Assume 1000,00
                        val_str = val_str.replace(',', '.')
                    # else assume 1000.00
                    
                    amount = float(val_str)
            except Exception as e:
                print(f"Amount parse error: {e}")
                amount = 0.0
            
            # Critical: Ensure amount is not NaN (pandas might return nan float)
            import math
            if isinstance(amount, float) and math.isnan(amount):
                amount = 0.0

            # 3. Description & Subcategory from 'Category' column if useful
            description = row.get('Concepto', 'No description')
            raw_category = row.get('Categoría', None)
            
            # Append raw category to description or subcategory field if we wanted
            # For now, let's just make sure description is clean
            description = str(description).strip()
            
            # Create object
            transaction = TransactionCreate(
                date=date_obj,
                amount=amount,
                description=description,
                subcategory=str(raw_category) if pd.notna(raw_category) else None,
                account_id=account_id,
                raw_import_data=str(row.to_dict())
            )
            transactions.append(transaction)
            
        return transactions
