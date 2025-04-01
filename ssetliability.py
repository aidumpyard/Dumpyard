# Re-import libraries due to reset
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

# Step 1: Filter by Entity-Cpty Entity pair + Business Date > 5M
def filter_entity_date_pairs(df, threshold=5_000_000):
    df["pair_key"] = df.apply(lambda row: tuple(sorted([row["Entity"], row["Cpty Entity"]])), axis=1)
    group_totals = df.groupby(["pair_key", "Business Date"])["Amount"].sum()
    valid_keys = group_totals[group_totals > threshold].index
    df_filtered = df.set_index(["pair_key", "Business Date"]).loc[valid_keys].reset_index()
    df_filtered = df_filtered.drop(columns=["pair_key"])
    return df_filtered

# Step 2: Remove both Asset and matching Liability if paired
def match_and_remove_pairs(df):
    matched_asset_indices = set()
    matched_liability_indices = set()

    assets = df[df["ALI"] == "Assets"]
    liabilities = df[df["ALI"] == "Liabilities"]

    for i, asset in assets.iterrows():
        for j, liability in liabilities.iterrows():
            if (
                asset["Amount"] == liability["Amount"]
                and asset["Entity"] == liability["Cpty Entity"]
                and asset["Cpty Entity"] == liability["Entity"]
                and asset["Business Date"] == liability["Business Date"]
            ):
                matched_asset_indices.add(i)
                matched_liability_indices.add(j)
                break

    all_matched_indices = matched_asset_indices.union(matched_liability_indices)
    df_cleaned = df.drop(index=all_matched_indices)
    return df_cleaned

# Apply filtering and matching
filtered_df = filter_entity_date_pairs(df)
final_cleaned_df = match_and_remove_pairs(filtered_df)

import ace_tools as tools; tools.display_dataframe_to_user(name="Cleaned Final Data", dataframe=final_cleaned_df)

final_cleaned_df