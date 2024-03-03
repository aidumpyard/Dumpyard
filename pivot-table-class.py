import csv
import threading
from concurrent.futures import ThreadPoolExecutor
import win32com.client as win32

class WorkbookManager:
    def __init__(self):
        self.excel = win32.gencache.EnsureDispatch('Excel.Application')
        self.open_workbooks = {}

    def get_workbook(self, file_path, read_only=True):
        if file_path not in self.open_workbooks:
            self.open_workbooks[file_path] = self.excel.Workbooks.Open(file_path, ReadOnly=read_only)
        return self.open_workbooks[file_path]

    def close_workbook(self, file_path):
        if file_path in self.open_workbooks:
            self.open_workbooks[file_path].Close()
            del self.open_workbooks[file_path]

    def close_all(self):
        for wb in self.open_workbooks.values():
            wb.Close()
        self.open_workbooks.clear()
        self.excel.Quit()

class PivotTableUpdater:
    def __init__(self, wb_manager):
        self.wb_manager = wb_manager

    def update_pivot_table(self, pivot_config):
        try:
            pivot_wb = self.wb_manager.get_workbook(pivot_config['pivot_file_path'], read_only=False)
            data_wb = self.wb_manager.get_workbook(pivot_config['data_file_path'], read_only=True)

            pivot_sheet = pivot_wb.Sheets(pivot_config['pivot_sheet_name'])
            pivot_table = pivot_sheet.PivotTables(pivot_config['pivot_table_name'])

            new_data_range = f'[{data_wb.Name}]' + pivot_config['data_sheet_name'] + '!' + pivot_config['data_range']
            pivot_table.ChangePivotCache(pivot_wb.PivotCaches().Create(SourceType=win32.constants.xlDatabase, SourceData=new_data_range))

            pivot_wb.Save()
            return "OK"
        except Exception as e:
            return f"Not OK - {e}"

def main():
    wb_manager = WorkbookManager()
    updater = PivotTableUpdater(wb_manager)

    with open('pivot_table_config.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        rows = [row for row in csv_reader if row['status'].lower() == 'active']

    max_threads = 4  # Adjust this value based on the desired number of threads
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(updater.update_pivot_table, row) for row in rows]
        for i, future in enumerate(futures):
            rows[i]['last_run_status'] = future.result()
            wb_manager.close_workbook(rows[i]['pivot_file_path'])

    wb_manager.close_all()

    with open('pivot_table_status.csv', mode='w', newline='') as file:
        fieldnames = csv_reader.fieldnames + ['last_run_status']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

if __name__ == '__main__':
    main()