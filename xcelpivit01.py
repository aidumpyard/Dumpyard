import win32com.client as win32

# Open Excel and the workbook
excel = win32.gencache.EnsureDispatch('Excel.Application')
wb = excel.Workbooks.Open(r'path\to\your\workbook.xlsx')

# Select the sheet with the pivot table
sheet = wb.Sheets('SheetWithPivotTable')

# Get the pivot table
pivot_table = sheet.PivotTables('YourPivotTableName')

# Define the new data source range
new_data_range = 'SheetWithData!A1:D100'  # Adjust this to your new data range

# Change the pivot table data source
pivot_table.ChangePivotCache(wb.PivotCaches().Create(SourceType=win32.constants.xlDatabase, SourceData=new_data_range))

# Save and close
wb.Save()
wb.Close()
excel.Quit()