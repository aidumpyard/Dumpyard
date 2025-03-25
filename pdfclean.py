import pdfplumber
import pandas as pd

pdf_path = "your_file.pdf"  # Replace with your actual file path

rows = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            for line in text.split("\n"):
                rows.append(line.strip())  # Store each line

# Display raw lines (optional)
for i, row in enumerate(rows[:5]):
    print(f"Row {i}: {row}")

# Assuming the data is comma-separated (CSV-like)
df = pd.DataFrame([line.split(",") for line in rows])

print(df.head())