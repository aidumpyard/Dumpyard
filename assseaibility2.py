# Re-import libraries due to environment reset
from PIL import Image
import pytesseract
import pandas as pd

# Manually reconstruct the table based on the image again
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

# Step 1: Filter by entity pair total value > 5 million
def filter_entity_pairs(df, threshold=5_000_000):
    df["pair_key"] = df.apply(lambda row: tuple(sorted([row["Entity"], row["Cpty Entity"]])), axis=1)
    pair_totals = df.groupby("pair_key")["Amount"].sum()
    valid_keys = pair_totals[pair_totals > threshold].index
    filtered_df = df[df["pair_key"].isin(valid_keys)].drop(columns=["pair_key"])
    return filtered_df

# Step 2: Match asset-liability records
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

# Apply filtering and then matching
filtered_by_pair_df = filter_entity_pairs(df)
final_filtered_df = match_and_filter(filtered_by_pair_df)

import ace_tools as tools; tools.display_dataframe_to_user(name="Filtered & Matched Records", dataframe=final_filtered_df)

final_filtered_df