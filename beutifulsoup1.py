import win32com.client
import pandas as pd
from bs4 import BeautifulSoup

# Connect to Outlook
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

# Access Inbox (or specific folder if needed)
inbox = outlook.GetDefaultFolder(6)  # 6 refers to the inbox

# Search for emails with "IC Funding" in subject
messages = inbox.Items
messages = messages.Restrict("[Subject] LIKE 'IC Funding*'")
messages.Sort("[ReceivedTime]", True)  # Sort by newest first

latest_email = None
previous_email = None

# Find the latest email with "Approved."
for message in messages:
    if "Approved." in message.Body:
        latest_email = message
        break

# If latest email found, get the previous one
if latest_email:
    for message in messages:
        if message.ReceivedTime < latest_email.ReceivedTime:
            previous_email = message
            break

# Extract table from the previous email
if previous_email:
    # Get the email HTML body
    html_body = previous_email.HTMLBody

    # Parse with BeautifulSoup
    soup = BeautifulSoup(html_body, "html.parser")
    table = soup.find("table")  # Locate the table

    # Extract data
    rows = table.find_all("tr")
    data = []
    headers = [th.text.strip() for th in rows[0].find_all("th")]

    for row in rows[1:]:
        data.append([td.text.strip() for td in row.find_all("td")])

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=headers)

    # Save to Excel
    excel_path = "C:\\path\\to\\save\\Intercompany_Funding_Approval.xlsx"
    df.to_excel(excel_path, index=False)

    print(f"Table extracted and saved successfully at {excel_path}")

else:
    print("No previous email found with a table.")