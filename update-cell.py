import csv
import win32com.client as win32

def update_pivot_table(pivot_config):
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    try:
        pivot_wb = excel.Workbooks.Open(pivot_config['pivot_file_path'], ReadOnly=False)
        data_wb = excel.Workbooks.Open(pivot_config['data_file_path'], ReadOnly=True)

        pivot_sheet = pivot_wb.Sheets(pivot_config['pivot_sheet_name'])
        pivot_table = pivot_sheet.PivotTables(pivot_config['pivot_table_name'])

        new_data_range = f'[{data_wb.Name}]' + pivot_config['data_sheet_name'] + '!' + pivot_config['data_range']
        pivot_table.ChangePivotCache(pivot_wb.PivotCaches().Create(SourceType=win32.constants.xlDatabase, SourceData=new_data_range))

        # Update pivot sheet cell with data file path if required
        if pivot_config['WriteCellStatus'].lower() == 'yes':
            write_cell = pivot_config['WriteCellNumber']
            pivot_sheet.Range(write_cell).Value = pivot_config['data_file_path']

        pivot_wb.Save()
        pivot_wb.Close()
        data_wb.Close(False)  # Close the data workbook without saving
        return "OK"
    except Exception as e:
        return f"Not OK - {e}"
    finally:
        excel.Quit()

def main():
    with open('PivotTableUpdate.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        status_list = []
        for row in csv_reader:
            if row['status'].lower() == 'active':
                status = update_pivot_table(row)
                row['last_run_status'] = status
                status_list.append(row)

    with open('pivot_table_status.csv', mode='w', newline='') as file:
        fieldnames = csv_reader.fieldnames + ['last_run_status']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(status_list)

if __name__ == '__main__':
    main()