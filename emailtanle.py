import win32com.client
from bs4 import BeautifulSoup
import pandas as pd
import xlsxwriter

# Step 1: Connect to Outlook and get the HTML body
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6)  # 6 = Inbox
messages = inbox.Items
messages.Sort("[ReceivedTime]", True)

for message in messages:
    if "ALM NPV" in message.Subject and message.Class == 43:
        html_body = message.HTMLBody
        break
else:
    raise Exception("Target email not found")

# Step 2: Extract the first table from HTML
soup = BeautifulSoup(html_body, "html.parser")
table = soup.find("table")

# Step 3: Parse table into list of lists
rows = table.find_all("tr")
table_data = [[col.get_text(strip=True) for col in row.find_all(["th", "td"])] for row in rows]

# Step 4: Write to Excel using xlsxwriter
workbook = xlsxwriter.Workbook("ALM_NPV_Email_Table.xlsx")
worksheet = workbook.add_worksheet("Email Table")

# Optional formatting
header_format = workbook.add_format({'bold': True, 'bg_color': '#DDEBF7', 'border': 1})
cell_format = workbook.add_format({'border': 1})

for row_idx, row_data in enumerate(table_data):
    for col_idx, cell in enumerate(row_data):
        fmt = header_format if row_idx == 0 else cell_format
        worksheet.write(row_idx, col_idx, cell, fmt)

workbook.close()

print("Email table written with formatting to: ALM_NPV_Email_Table.xlsx")