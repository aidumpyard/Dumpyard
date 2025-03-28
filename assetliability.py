# Manually reconstruct the table based on the OCR and visible content from the image

data = [
    ["Deposits", "Loans", "3/13/2025", "Deutsche Bank", "Deutsche Bank Aktier", "USD", "Liabilities", "M6", 123, 3.32E+08],
    ["Deposits", "Loans", "3/13/2025", "Deutsche Bank", "Reporting Company", "USD", "Liabilities", "OVER2Y", 2528, 7.17E+08],
    ["Loans", "Deposits", "3/13/2025", "Deutsche Bank", "Deutsche Bank Aktier", "USD", "Assets", "M6", 123, 3.32E+08],
    ["Deposits", "Loans", "3/13/2025", "Deutsche Bank", "Deutsche Bank Aktier", "EUR", "Liabilities", "M6", 123, 3.28E+08],
    ["Loans", "Deposits", "3/13/2025", "Reporting Com", "Deutsche Bank Aktier", "USD", "Assets", "OVER2Y", 2528, 7.17E+08],
    ["Deposits", "Loans", "3/13/2025", "Deutsche Bank", "Deutsche Bank Aktier", "USD", "Liabilities", "M15", 399, 3.32E+08],
    ["Deposits", "Loans", "3/13/2025", "Reporting Com", "Deutsche Bank Aktier", "USD", "Liabilities", "OVER2Y", 2528, 7.17E+08],
]

columns = [
    "LE_View", "CP_View", "Business Date", "Entity", "Cpty Entity", "Currency Name",
    "ALI", "Time Bucket", "tenor", "Amount"
]

df = pd.DataFrame(data, columns=columns)

# Function to identify matching asset-liability pairs
def match_and_filter(df):
    matched_indices = set()
    final_records = []

    for i, asset in df[df["ALI"] == "Assets"].iterrows():
        for j, liability in df[df["ALI"] == "Liabilities"].iterrows():
            if (
                asset["Amount"] == liability["Amount"]
                and asset["Entity"] == liability["Cpty Entity"]
                and asset["Cpty Entity"] == liability["Entity"]
                and asset["Business Date"] == liability["Business Date"]
            ):
                matched_indices.add(j)
                final_records.append(asset)
                break
        else:
            final_records.append(asset)

    # Add unmatched liabilities
    for i, row in df[df["ALI"] == "Liabilities"].iterrows():
        if i not in matched_indices:
            final_records.append(row)

    return pd.DataFrame(final_records)

filtered_df = match_and_filter(df)

import ace_tools as tools; tools.display_dataframe_to_user(name="Filtered Asset-Liability Data", dataframe=filtered_df)

filtered_df