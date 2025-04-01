# Reconstruct the original data again after kernel reset
data = [
    ["Deposits", "Loans", "3/13/2025", "DB_CP_F", "DB_E_F", "USD", "Liabilities", "M6", 123, 3.32E+08],
    ["Deposits", "Loans", "3/13/2025", "DB001", "DB003", "USD", "Liabilities", "OVER2Y", 2528, 7.17E+08],
    ["Loans", "Deposits", "3/13/2025", "DB_E_F", "DB_CP_F", "USD", "Assets", "M6", 123, 3.32E+08],
    ["Deposits", "Loans", "3/13/2025", "DB004", "DB002", "EUR", "Liabilities", "M6", 123, 3.28E+08],
    ["Loans", "Deposits", "3/13/2025", "DB003", "DB001", "USD", "Assets", "OVER2Y", 2528, 7.17E+08],
    ["Deposits", "Loans", "3/13/2025", "DBLND", "DBNY", "USD", "Liabilities", "M15", 399, 3.32E+08],
    ["Deposits", "Loans", "3/13/2025", "DB003", "DB002", "USD", "Liabilities", "OVER2Y", 2528, 7.17E+08],
]

columns = [
    "LE_View", "CP_View", "Business Date", "Entity", "Cpty Entity", "Currency Name",
    "ALI", "Time Bucket", "tenor", "Amount"
]

df = pd.DataFrame(data, columns=columns)

# Step 1: Filter entity-cpty entity pair by business date and total amount > 5 million
def filter_entity_date_pairs(df, threshold=5_000_000):
    df["pair_key"] = df.apply(lambda row: tuple(sorted([row["Entity"], row["Cpty Entity"]])), axis=1)
    group_totals = df.groupby(["pair_key", "Business Date"])["Amount"].sum()
    valid_keys = group_totals[group_totals > threshold].index
    df_filtered = df.set_index(["pair_key", "Business Date"]).loc[valid_keys].reset_index()
    df_filtered = df_filtered.drop(columns=["pair_key"])
    return df_filtered

# Step 2: Match asset-liability and keep only asset if matched
def match_and_keep_assets(df):
    matched_liability_indices = set()
    matched_asset_indices = set()

    for i, asset in df[df["ALI"] == "Assets"].iterrows():
        for j, liability in df[df["ALI"] == "Liabilities"].iterrows():
            if (
                asset["Amount"] == liability["Amount"]
                and asset["Entity"] == liability["Cpty Entity"]
                and asset["Cpty Entity"] == liability["Entity"]
                and asset["Business Date"] == liability["Business Date"]
            ):
                matched_liability_indices.add(j)
                matched_asset_indices.add(i)
                break

    # Keep all assets and unmatched liabilities
    kept_df = df.drop(index=matched_liability_indices)
    return kept_df

# Apply filtering and asset-keeping logic
filtered_df = filter_entity_date_pairs(df)
final_asset_df = match_and_keep_assets(filtered_df)

import ace_tools as tools; tools.display_dataframe_to_user(name="Matched Pairs (Assets Kept)", dataframe=final_asset_df)

final_asset_df