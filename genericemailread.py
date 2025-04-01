import win32com.client
from bs4 import BeautifulSoup
import pandas as pd
import xlsxwriter
from datetime import datetime

# --- Config ---
SUBJECT_KEYWORDS = ["ALM NPV", "SLR NPV", "TMI NPV"]
TARGET_DATE = datetime.today().date()  # Change if needed
OUTPUT_FILE = "NPV_Tables_By_Subject.xlsx"

# --- Connect to Outlook ---
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6)
messages = inbox.Items
messages.Sort("[ReceivedTime]", True)

# --- Prepare Workbook ---
workbook = xlsxwriter.Workbook(OUTPUT_FILE)

# Format definitions
header_format = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#DDEBF7', 'border': 1})
sub_header_format = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#FCE4D6', 'border': 1})
cell_format = workbook.add_format({'border': 1})

# --- Process Emails by Subject ---
found_subjects = set()

for message in messages:
    subject = message.Subject
    received = message.ReceivedTime.date()

    for keyword in SUBJECT_KEYWORDS:
        if keyword in subject and message.Class == 43 and received == TARGET_DATE and keyword not in found_subjects:
            html_body = message.HTMLBody
            soup = BeautifulSoup(html_body, "html.parser")
            table = soup.find("table")

            if not table:
                continue  # skip if no table

            rows = table.find_all("tr")
            table_data = [[col.get_text(strip=True) for col in row.find_all(["th", "td"])] for row in rows]

            if not table_data or len(table_data[0]) < 10:
                continue  # skip malformed tables

            # --- Write to Excel Sheet ---
            sheet = workbook.add_worksheet(keyword.replace(" ", "_"))
            sheet.write(0, 0, "ALM", header_format)
            sheet.merge_range(0, 1, 0, 3, "MTD", header_format)
            sheet.merge_range(0, 4, 0, 6, "QTD", header_format)
            sheet.merge_range(0, 7, 0, 9, "YTD", header_format)

            sub_headers = ["Delta", "Sales", "Accr"] * 3
            for i, header in enumerate(sub_headers):
                sheet.write(1, i + 1, header, sub_header_format)
            sheet.write(1, 0, "", sub_header_format)

            for row_idx, row_data in enumerate(table_data[1:], start=2):
                for col_idx, cell in enumerate(row_data):
                    sheet.write(row_idx, col_idx, cell, cell_format)

            sheet.set_column(0, 9, 12)
            found_subjects.add(keyword)

workbook.close()
print(f"Done! Tables written to: {OUTPUT_FILE}")