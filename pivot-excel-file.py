import win32com.client as win32

def change_pivot_table_data_source(pivot_file_path, data_file_path, pivot_sheet_name, pivot_table_name, data_sheet_name, data_range):
    # Open Excel
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    
    # Open the workbook with the pivot table
    pivot_wb = excel.Workbooks.Open(pivot_file_path)
    
    # Open the workbook with the new data range
    data_wb = excel.Workbooks.Open(data_file_path)
    
    # Get the sheet with the pivot table
    pivot_sheet = pivot_wb.Sheets(pivot_sheet_name)
    
    # Get the pivot table
    pivot_table = pivot_sheet.PivotTables(pivot_table_name)
    
    # Define the new data range from the other workbook
    new_data_range = f'[{data_wb.Name}]' + data_sheet_name + '!' + data_range
    
    # Change the pivot table data source
    pivot_table.ChangePivotCache(pivot_wb.PivotCaches().Create(SourceType=win32.constants.xlDatabase, SourceData=new_data_range))
    
    # Save and close
    pivot_wb.Save()
    pivot_wb.Close()
    data_wb.Close()
    excel.Quit()

# Example usage
pivot_file_path = r'path\to\pivot_table_workbook.xlsx'
data_file_path = r'path\to\new_data_workbook.xlsx'
pivot_sheet_name = 'SheetWithPivotTable'
pivot_table_name = 'YourPivotTableName'
data_sheet_name = 'SheetWithData'
data_range = 'A1:D100'

change_pivot_table_data_source(pivot_file_path, data_file_path, pivot_sheet_name, pivot_table_name, data_sheet_name, data_range)