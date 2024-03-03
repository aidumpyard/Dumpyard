import csv
import win32com.client as win32
from datetime import datetime

def update_pivot_table(pivot_file_path, pivot_sheet_name, pivot_table_name, data_file_path, data_sheet_name, data_range):
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    try:
        pivot_wb = excel.Workbooks.Open(pivot_file_path, ReadOnly=False)
        data_wb = excel.Workbooks.Open(data_file_path, ReadOnly=True)

        pivot_sheet = pivot_wb.Sheets(pivot_sheet_name)
        pivot_table = pivot_sheet.PivotTables(pivot_table_name)

        new_data_range = f'[{data_wb.Name}]' + data_sheet_name + '!' + data_range
        pivot_table.ChangePivotCache(pivot_wb.PivotCaches().Create(SourceType=win32.constants.xlDatabase, SourceData=new_data_range))

        pivot_wb.Save()
        pivot_wb.Close()
        data_wb.Close()
        excel.Quit()
        return "Status: OK"
    except Exception as e:
        excel.Quit()
        return f"Status: Not OK - {e}"

def send_email(email_id, status_list):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = email_id
    current_date = datetime.now().strftime('%Y-%m-%d')
    mail.Subject = f'Pivot Tables Update - {current_date}'

    body = "Pivot Tables Update Status:\n\n"
    for status in status_list:
        body += f"{status['pivot_file_path']} - {status['status']}\n"
    body += "\nPlease check the attached status file for more details."

    mail.Body = body
    mail.Attachments.Add('path\\to\\pivot_table_status.csv')
    mail.Send()

def main():
    status_list = []

    with open('pivot_table_config.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['status'].lower() == 'active':
                status = update_pivot_table(
                    row['pivot_file_path'],
                    row['pivot_sheet_name'],
                    row['pivot_table_name'],
                    row['data_file_path'],
                    row['data_sheet_name'],
                    row['data_range']
                )
                status_list.append({'pivot_file_path': row['pivot_file_path'], 'status': status})

    with open('pivot_table_status.csv', mode='w', newline='') as file:
        fieldnames = ['pivot_file_path', 'status']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(status_list)

    with open('PivotTableEmail.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['email_send_status'].lower() == 'yes':
                send_email(row['email_id'], status_list)

if __name__ == '__main__':
    main()

email_id,email_send_status
example@email.com,yes
    
