import pandas as pd
import os

# Load the email dump data
email_dump = pd.read_csv("email_dump.csv")  # Adjust filename as needed
main_df = pd.read_csv("main_df.csv")        # Adjust filename as needed

# Load the existing Excel file
file_path = "IMCS.xlsx"
sheet_name = "Sheet2"

# Read the Excel sheet
with pd.ExcelFile(file_path) as xls:
    df_excel = pd.read_excel(xls, sheet_name=sheet_name)

# Ensure Approval column exists
if "Approval" not in df_excel.columns:
    df_excel["Approval"] = ""

# Define the columns for matching
entity_col = "entity"
cpty_col = "cpty_name"
filepath_col = "filepath"

# Merge new records from email_dump based on conditions
for _, email_row in email_dump.iterrows():
    entity_match = main_df[entity_col] == email_row[entity_col]
    cpty_match = main_df[cpty_col] == email_row[cpty_col]

    matched_records = main_df[entity_match & cpty_match]

    if not matched_records.empty:
        for _, matched_row in matched_records.iterrows():
            # Append new record with Approval column
            new_record = matched_row.to_dict()
            new_record["Approval"] = email_row[filepath_col]  # Assign the .msg file path

            # Append to DataFrame
            df_excel = pd.concat([df_excel, pd.DataFrame([new_record])], ignore_index=True)

# Save the updated Excel file
with pd.ExcelWriter(file_path, mode="a", if_sheet_exists="replace") as writer:
    df_excel.to_excel(writer, sheet_name=sheet_name, index=False)

print("Records updated successfully!")