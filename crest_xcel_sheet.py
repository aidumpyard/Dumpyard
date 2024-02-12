import pandas as pd
import os

# Assuming df1 and df2 are already defined
# df1 = ...
# df2 = ...

filename = 'master.xlsx'

# Function to check if sheet exists in the workbook
def sheet_exists(workbook, sheet_name):
    return sheet_name in workbook.sheetnames

# Function to save a dataframe to a specific sheet, without overwriting other sheets
def save_df_to_sheet(df, writer, sheet_name):
    df.to_excel(writer, sheet_name=sheet_name, index=False)

# Check if the file exists
if os.path.exists(filename):
    # Load the workbook and the existing sheets
    with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        book = writer.book
        
        # Check for 'master' sheet and concatenate df1 if it exists
        if sheet_exists(book, 'master'):
            master_df = pd.read_excel(filename, sheet_name='master')
            updated_master_df = pd.concat([master_df, df1], ignore_index=True)
            save_df_to_sheet(updated_master_df, writer, 'master')
        else:
            # If 'master' sheet does not exist, create it and write df1
            save_df_to_sheet(df1, writer, 'master')
        
        # Check for 'file_info' sheet and concatenate df2 if it exists
        if sheet_exists(book, 'file_info'):
            file_info_df = pd.read_excel(filename, sheet_name='file_info')
            updated_file_info_df = pd.concat([file_info_df, df2], ignore_index=True)
            save_df_to_sheet(updated_file_info_df, writer, 'file_info')
        else:
            # If 'file_info' sheet does not exist, create it and write df2
            save_df_to_sheet(df2, writer, 'file_info')
else:
    # If the file does not exist, create it and write both df1 and df2 to separate sheets
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        save_df_to_sheet(df1, writer, 'master')
        save_df_to_sheet(df2, writer, 'file_info')