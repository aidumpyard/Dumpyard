# Re-import libraries after code execution state reset
import pandas as pd

# Reconstruct original data
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

# Step 1: Filter based on Entity-Cpty Entity pair and Business Date with total amount > 5 million
def filter_entity_date_pairs(df, threshold=5_000_000):
    df["pair_key"] = df.apply(lambda row: tuple(sorted([row["Entity"], row["Cpty Entity"]])), axis=1)
    group_totals = df.groupby(["pair_key", "Business Date"])["Amount"].sum()
    valid_keys = group_totals[group_totals > threshold].index
    df_filtered = df.set_index(["pair_key", "Business Date"]).loc[valid_keys].reset_index()
    df_filtered = df_filtered.drop(columns=["pair_key"])
    return df_filtered

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

    for i, row in df[df["ALI"] == "Liabilities"].iterrows():
        if i not in matched_indices:
            final_records.append(row)

    return pd.DataFrame(final_records)

# Apply the filtering and matching logic
filtered_by_entity_date = filter_entity_date_pairs(df)
final_df = match_and_filter(filtered_by_entity_date)

import ace_tools as tools; tools.display_dataframe_to_user(name="Final Filtered Data", dataframe=final_df)

final_df