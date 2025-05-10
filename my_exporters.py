import pandas as pd

def export_to_csv(df: pd.DataFrame, filename='results.csv'):
    df.to_csv(filename, index=False)

def export_to_excel(df: pd.DataFrame, filename='results.xlsx'):
    df.to_excel(filename, index=False)

def export_to_ris(df: pd.DataFrame, filename='results.ris'):
    # Basic RIS export
    with open(filename, 'w') as f:
        for _, row in df.iterrows():
            f.write("TY  - JOUR\n")
            f.write(f"TI  - {row.get('Title','')}\n")
            f.write(f"AU  - {row.get('Author','')}\n")
            f.write(f"JO  - {row.get('Journal','')}\n")
            f.write(f"PY  - {row.get('Date','')}\n")
            if row.get('DOI'): f.write(f"DO  - {row.get('DOI')}\n")
            f.write("ER  - \n\n")
