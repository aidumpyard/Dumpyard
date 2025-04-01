import win32com.client
from bs4 import BeautifulSoup
import pandas as pd
import xlsxwriter

# Step 1: Connect to Outlook and get the HTML body
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6)
messages = inbox.Items
messages.Sort("[ReceivedTime]", True)

for message in messages:
    if "ALM NPV" in message.Subject and message.Class == 43:
        html_body = message.HTMLBody
        break
else:
    raise Exception("Target email not found")

# Step 2: Parse the first table
soup = BeautifulSoup(html_body, "html.parser")
table = soup.find("table")

rows = table.find_all("tr")
table_data = [[col.get_text(strip=True) for col in row.find_all(["th", "td"])] for row in rows]

# Step 3: Write to Excel with merged headers
workbook = xlsxwriter.Workbook("ALM_NPV_Email_Merged.xlsx")
worksheet = workbook.add_worksheet("ALM Table")

# Format definitions
header_format = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#DDEBF7', 'border': 1})
sub_header_format = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#FCE4D6', 'border': 1})
cell_format = workbook.add_format({'border': 1})

# Example columns: 1 fixed column + 3 sets of MTD, QTD, YTD (each has 3)
worksheet.write(0, 0, "ALM", header_format)
worksheet.merge_range(0, 1, 0, 3, "MTD", header_format)
worksheet.merge_range(0, 4, 0, 6, "QTD", header_format)
worksheet.merge_range(0, 7, 0, 9, "YTD", header_format)

# Subheaders row (Row 1)
sub_headers = ["Delta", "Sales", "Accr"] * 3
for i, header in enumerate(sub_headers):
    worksheet.write(1, i + 1, header, sub_header_format)
worksheet.write(1, 0, "", sub_header_format)  # empty under "ALM"

# Data starts from row 2
for row_idx, row_data in enumerate(table_data[1:], start=2):  # skipping header row
    for col_idx, cell in enumerate(row_data):
        worksheet.write(row_idx, col_idx, cell, cell_format)

# Optional: Auto-fit column widths
worksheet.set_column(0, 9, 12)

workbook.close()
print("Table with merged headers written to ALM_NPV_Email_Merged.xlsx")