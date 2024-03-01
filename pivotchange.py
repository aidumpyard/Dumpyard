import win32com.client as win32

# Open Excel
excel = win32.gencache.EnsureDispatch('Excel.Application')

# Open the workbook with the pivot table
pivot_wb = excel.Workbooks.Open(r'path\to\pivot_table_workbook.xlsx')

# Open the workbook with the new data range
data_wb = excel.Workbooks.Open(r'path\to\new_data_workbook.xlsx')

# Get the sheet with the pivot table
pivot_sheet = pivot_wb.Sheets('SheetWithPivotTable')

# Get the pivot table
pivot_table = pivot_sheet.PivotTables('YourPivotTableName')

# Define the new data range from the other workbook
new_data_range = f'[{data_wb.Name}]SheetWithData!A1:D100'  # Adjust the sheet name and range

# Change the pivot table data source
pivot_table.ChangePivotCache(pivot_wb.PivotCaches().Create(SourceType=win32.constants.xlDatabase, SourceData=new_data_range))

# Save and close
pivot_wb.Save()
pivot_wb.Close()
data_wb.Close()
excel.Quit()