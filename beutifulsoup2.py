import win32com.client
import pandas as pd
from bs4 import BeautifulSoup

# Connect to Outlook
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

# Access Inbox
inbox = outlook.GetDefaultFolder(6)  # 6 refers to the inbox
messages = inbox.Items

# Sort messages by ReceivedTime (Descending)
messages.Sort("[ReceivedTime]", True)

latest_email = None
previous_email = None

# Iterate through the last 50 emails to find "Approved."
for message in list(messages)[:50]:  # Restrict to last 50 emails to avoid performance issues
    if "Approved." in message.Body:
        latest_email = message
        break

# Find the previous email in the same thread
if latest_email:
    latest_received_time = latest_email.ReceivedTime
    for message in list(messages)[:50]:
        if message.ReceivedTime < latest_received_time:
            previous_email = message
            break

# Extract table from the previous email
if previous_email:
    # Get the email HTML body
    html_body = previous_email.HTMLBody

    # Parse with BeautifulSoup
    soup = BeautifulSoup(html_body, "html.parser")
    table = soup.find("table")  # Locate the first table

    if table:
        # Extract table rows
        rows = table.find_all("tr")
        data = []
        
        # Extract headers (if available)
        headers = [th.text.strip() for th in rows[0].find_all("th")]
        if not headers:
            headers = [td.text.strip() for td in rows[0].find_all("td")]  # If no <th>, use first row <td>

        # Extract data rows
        for row in rows[1:]:
            data.append([td.text.strip() for td in row.find_all("td")])

        # Convert to DataFrame
        df = pd.DataFrame(data, columns=headers)

        # Save to Excel
        excel_path = "C:\\path\\to\\save\\Intercompany_Funding_Approval.xlsx"
        df.to_excel(excel_path, index=False)

        print(f"Table extracted and saved successfully at {excel_path}")
    else:
        print("No table found in the previous email.")
else:
    print("No previous email found with a table.")