import pdfplumber
import pandas as pd

pdf_path = "your_file.pdf"  # Replace with your PDF file path

all_tables = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            df = pd.DataFrame(table[1:], columns=table[0])
            all_tables.append(df)

# Combine all tables into one DataFrame (optional)
final_df = pd.concat(all_tables, ignore_index=True)

print(final_df)