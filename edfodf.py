import pandas as pd

# Sample data (replace with actual data loading)
edf_data = {
    'received': ['2024-03-01', '2024-03-02', '2024-03-04'],
    'subject': ['sub1', 'sub2', 'sub3'],
    'entity': ['A', 'B', 'C'],
    'cpEntity': ['X', 'Y', 'Z'],
    'amount': [100, 200, 300],
    'filepath': ['path1', 'path2', 'path3']
}

odf_data = {
    'Product': ['Loans', 'Deposits', 'Loans', 'Deposits'],
    'Date': ['2024-03-01', '2024-03-02', '2024-03-02', '2024-03-04'],
    'Entity': ['A', 'B', 'B', 'C'],
    'CpEntity': ['X', 'Y', 'Y', 'Z'],
    'Amount': [100, 200, 200, 300],
    'Status': ['Active', 'Active', 'Active', 'Active']
}

edf = pd.DataFrame(edf_data)
odf = pd.DataFrame(odf_data)

# Convert date columns to datetime
edf['received'] = pd.to_datetime(edf['received'])
odf['Date'] = pd.to_datetime(odf['Date'])

# Step 1: Process odf to remove duplicates based on conditions
odf_sorted = odf.sort_values(by=['Product'], ascending=False)  # Sort to keep 'Loans' over 'Deposits'
odf_unique = odf_sorted.drop_duplicates(subset=['Date', 'Entity', 'CpEntity', 'Amount', 'Status'], keep='first')

# Step 2: Swap 'Entity' and 'CpEntity' for 'Deposits' and negate 'Amount'
for index, row in odf_unique.iterrows():
    if row['Product'] == 'Deposits':
        odf_unique.at[index, 'Entity'], odf_unique.at[index, 'CpEntity'] = row['CpEntity'], row['Entity']
        odf_unique.at[index, 'Amount'] = -row['Amount']

# Step 3: Merge edf and odf using an outer join to keep all odf values
merged_df = odf_unique.merge(
    edf,
    left_on=['Entity', 'CpEntity', 'Amount'],
    right_on=['entity', 'cpEntity', 'amount'],
    how='left'
)

# Step 4: Filter where 'received' is within 'Date + 2 days'
merged_df = merged_df[
    merged_df['received'].isna() | ((merged_df['received'] >= merged_df['Date']) & (merged_df['received'] <= merged_df['Date'] + pd.Timedelta(days=2)))
]

# Step 5: Select final columns
output_df = merged_df[['Date', 'Entity', 'CpEntity', 'Amount', 'Status', 'received', 'subject', 'filepath']]

# Display the result
import ace_tools as tools
tools.display_dataframe_to_user(name="Processed Output", dataframe=output_df)