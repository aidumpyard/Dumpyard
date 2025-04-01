import win32com.client
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Connect to Outlook
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6)  # 6 = Inbox
messages = inbox.Items
messages.Sort("[ReceivedTime]", True)  # Sort by most recent first

# Step 2: Find the target email (you can filter by subject, sender, etc.)
for message in messages:
    if "ALM NPV" in message.Subject and message.Class == 43:  # 43 = Mail Item
        html_body = message.HTMLBody
        break
else:
    raise Exception("Email with subject containing 'ALM NPV' not found.")

# Step 3: Parse the HTML body
soup = BeautifulSoup(html_body, "html.parser")
table = soup.find("table")

# Step 4: Extract headers and rows
rows = table.find_all("tr")
data = []

for row in rows:
    cols = row.find_all(["td", "th"])
    data.append([col.get_text(strip=True) for col in cols])

# Step 5: Create a DataFrame
df = pd.DataFrame(data[1:], columns=data[0])
print(df)