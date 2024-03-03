import csv
import win32com.client as win32

def update_pivot_table(pivot_file_path, pivot_sheet_name, pivot_table_name, data_file_path, data_sheet_name, data_range):
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    pivot_wb = excel.Workbooks.Open(pivot_file_path)
    data_wb = excel.Workbooks.Open(data_file_path)

    pivot_sheet = pivot_wb.Sheets(pivot_sheet_name)
    pivot_table = pivot_sheet.PivotTables(pivot_table_name)

    new_data_range = f'[{data_wb.Name}]' + data_sheet_name + '!' + data_range
    pivot_table.ChangePivotCache(pivot_wb.PivotCaches().Create(SourceType=win32.constants.xlDatabase, SourceData=new_data_range))

    pivot_wb.Save()
    pivot_wb.Close()
    data_wb.Close()
    excel.Quit()

with open('pivot_table_config.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        if row['status'].lower() == 'active':
            update_pivot_table(
                row['pivot_file_path'],
                row['pivot_sheet_name'],
                row['pivot_table_name'],
                row['data_file_path'],
                row['data_sheet_name'],
                row['data_range']
            )