import pandas as pd

# Assuming your raw data is in a CSV or Excel and loaded as:
# df = pd.read_excel('your_file.xlsx') or pd.read_csv()

# Sample column assumptions based on the pivot
# ['FTP Division', 'Plan Business', 'FTP Classification', 'FTP Period', 'P&L']

pivot_df = df.pivot_table(
    index=['FTP Division', 'Plan Business', 'FTP Classification'],
    columns='FTP Period',
    values='P&L',
    aggfunc='sum',
    fill_value=0,
    margins=True,  # adds Grand Total
    margins_name='Grand Total'
)

# Reset index if you want a flat structure
pivot_df = pivot_df.reset_index()

# Save to Excel (optional)
pivot_df.to_excel('pivot_output.xlsx', index=False)

print(pivot_df)