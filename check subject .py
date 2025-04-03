import re
import pandas as pd
from datetime import datetime

def parse_subject(subject, receive_date):
    entries = re.split(r'(?<=\))\s+', subject)
    header = entries[0]
    lines = entries[1:]
    results = []

    for line in lines:
        match = re.match(r'(\d\))?\s*(.*?)\s+(\w+)\s*—>\s*(\w+)\s*\$([\d.]+)\s*bn\s*(M\d+)', line)
        if match:
            type_text = match.group(2).strip()
            entity = match.group(3)
            cpty = match.group(4)
            amount = float(match.group(5))
            duration = match.group(6)
            results.append({
                'Receive Date': receive_date,
                'Type': type_text,
                'Entity': entity,
                'CptyEntity': cpty,
                'Amount': amount,
                'Duration': duration,
                'Subject': subject
            })
    return results

# Example use
subject_list = [
    "IC Funding 1) Early Termination DBCI —> DBUSA $0.6bn M63",
    "IC Funding 1) Early Termination DBCI —> DBUSA $0.6bn M63 2) Early Termination DBUSA —> DBSI $0.6 bn M63",
    "IC Funding 1) Early Termination DBCI —> DBUSA $0.6bn M63 2) Early Termination DBUSA —> DBSI $0.6 bn M63 3) New Term Funding DBFFT —> DBUSA $0.4bn M63"
]

receive_date = datetime.today().strftime('%Y-%m-%d')

parsed_data = []
for subj in subject_list:
    parsed_data.extend(parse_subject(subj, receive_date))

df = pd.DataFrame(parsed_data)
print(df)