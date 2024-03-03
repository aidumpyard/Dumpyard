def send_email(email_id, status_list):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = email_id
    current_date = datetime.now().strftime('%Y-%m-%d')
    mail.Subject = f'Pivot Tables Update - {current_date}'

    body = "For internal use only\n\nPivot Tables Update Status:\n\n"
    for status in status_list:
        body += f"{status['pivot_file_path']} - {status['status']}\n"
    body += "\nPlease check the attached status file for more details."

    mail.Body = body
    mail.Attachments.Add('path\\to\\pivot_table_status.csv')

    # Set the sensitivity to Private or Confidential
    mail.Sensitivity = 2  # Private
    # mail.Sensitivity = 3  # Confidential

    mail.Send()