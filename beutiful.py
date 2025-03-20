import imaplib
import email
from bs4 import BeautifulSoup
import pandas as pd

# Email credentials
EMAIL = "your_email@example.com"
PASSWORD = "your_password"
IMAP_SERVER = "imap.example.com"

# Connect to the email server
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL, PASSWORD)
mail.select("inbox")

# Search for emails in the thread
status, email_ids = mail.search(None, '(SUBJECT "IC Funding")')

email_ids = email_ids[0].split()
latest_email_id = email_ids[-1]  # Get the latest email

# Fetch and parse the latest email
status, data = mail.fetch(latest_email_id, "(RFC822)")
raw_email = data[0][1]
msg = email.message_from_bytes(raw_email)

# Check if it contains "Approved."
email_body = ""
for part in msg.walk():
    if part.get_content_type() == "text/html":
        email_body = part.get_payload(decode=True).decode()
        break

if "Approved." in email_body:
    # Get the previous email
    previous_email_id = email_ids[-2]
    status, data = mail.fetch(previous_email_id, "(RFC822)")
    raw_email = data[0][1]
    prev_msg = email.message_from_bytes(raw_email)

    # Extract the table from the previous email
    email_body = ""
    for part in prev_msg.walk():
        if part.get_content_type() == "text/html":
            email_body = part.get_payload(decode=True).decode()
            break

    # Parse HTML to extract the table
    soup = BeautifulSoup(email_body, "html.parser")
    table = soup.find("table")

    # Convert table to DataFrame
    rows = table.find_all("tr")
    data = []
    headers = [th.text.strip() for th in rows[0].find_all("th")]

    for row in rows[1:]:
        data.append([td.text.strip() for td in row.find_all("td")])

    df = pd.DataFrame(data, columns=headers)

    # Save to Excel
    df.to_excel("Intercompany_Funding_Approval.xlsx", index=False)

    print("Table extracted and saved successfully.")