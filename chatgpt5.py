import pandas as pd
import os
import win32com.client as win32
from openpyxl import load_workbook

# Load the dataframes
email_dump = pd.read_csv('email_dump.csv')  # Adjust path
main_df = pd.read_csv('main_df.csv')  # Adjust path

# Load the existing Excel file and sheet
excel_file = 'IMCS.xlsm'  # Must be .xlsm for VBA to work
wb = load_workbook(excel_file, keep_vba=True)
ws = wb['Sheet2']  # Replace with actual sheet name

# Merge dataframes based on condition
merged_df = email_dump.merge(
    main_df,
    left_on=['entity', 'cpty_name'],
    right_on=['entity', 'cpty_name'],
    how='inner'
)

# Store the full file path (needed for embedding in VBA)
merged_df['Approval'] = merged_df['filepath']

# Append new rows to the sheet
for r in merged_df.itertuples(index=False, name=None):
    ws.append(r)

# Save the updated file
wb.save(excel_file)
wb.close()

print("Data appended. Now executing VBA macro...")

# Run the VBA macro to embed .msg files
excel_app = win32.Dispatch("Excel.Application")
excel_app.Visible = False  # Keep Excel hidden

# Open the workbook
wb_vba = excel_app.Workbooks.Open(os.path.abspath(excel_file))

# Run the macro (Ensure the macro name is correct)
macro_name = "Sheet2.EmbedMsgFiles"  # Format: 'SheetName.MacroName'
excel_app.Application.Run(macro_name)

# Save and close
wb_vba.Save()
wb_vba.Close()
excel_app.Quit()

print("VBA macro executed successfully. .msg files embedded in Excel.")