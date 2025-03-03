import os
import re
import win32com.client
import pandas as pd
from datetime import datetime

# Define parameters
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6)  # 6 refers to Inbox

date1 = datetime(2024, 2, 1)  # Start Date
date2 = datetime(2024, 2, 28)  # End Date
search_subject = "Invoice"  # Subject to search
save_path = r"C:\Users\YourUsername\Documents\Saved_Emails"  # Change to your path

# Ensure the save directory exists
os.makedirs(save_path, exist_ok=True)

# Function to clean subject for valid filename
def clean_filename(subject):
    return re.sub(r'[<>:"/\\|?*]', '', subject)

# Iterate through emails
messages = inbox.Items
messages = messages.Restrict(f"[ReceivedTime] >= '{date1.strftime('%m/%d/%Y')}' AND [ReceivedTime] <= '{date2.strftime('%m/%d/%Y')}'")

email_data = []
sequence_no = 0

for message in messages:
    try:
        if search_subject.lower() in message.Subject.lower():
            received_time = message.ReceivedTime.strftime("%Y-%m-%d %H:%M:%S")
            subject = clean_filename(message.Subject)
            filename = f"{sequence_no}_{subject}.msg"
            file_path = os.path.join(save_path, filename)
            
            # Save email
            message.SaveAs(file_path, 3)  # 3 corresponds to .msg format
            
            # Store email details
            email_data.append([received_time, subject, sequence_no])
            sequence_no += 1
    except Exception as e:
        print(f"Error processing email: {e}")

# Create DataFrame
df = pd.DataFrame(email_data, columns=["Received Time", "Subject", "Sequence No"])

# Display the DataFrame
import ace_tools as tools
tools.display_dataframe_to_user(name="Email Details", dataframe=df)