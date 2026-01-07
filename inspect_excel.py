import pandas as pd

file_path = "backend/MovimientosBancoCaixa2025.xlsx"
try:
    df = pd.read_excel(file_path, header=None, nrows=10)
    for i, row in df.iterrows():
        clean_row = [str(x).strip() for x in row.values if pd.notna(x) and str(x).strip() != '']
        print(f"Row {i}: {clean_row}")
            
except Exception as e:
    print(f"Error: {e}")
