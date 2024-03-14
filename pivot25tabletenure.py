import pandas as pd

# Adjusted sample data including 'tenure'
data = {
    'tenure': [0] * 13 + [1] * 13,
    'margin': [-20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40] * 2,
    'CCY': ['USD', 'USD', 'USD', 'USD', 'EUR', 'EUR', 'USD', 'EUR', 'USD', 'USD', 'USD', 'USD', 'USD'] * 2,
    'notional': [200, 200, 200, 200, 100, 300, 400, 500, 600, 600, 600, 600, 600] * 2
}

# Create a DataFrame
df = pd.DataFrame(data)

# Define a custom range adjustment function
def adjust_range(margin):
    if margin < -10:
        return '<-10', '-10'
    elif margin >= 30:
        return '30', '30+'
    else:
        return f'{margin - (margin % 5)}', f'{margin - (margin % 5) + 5}'

# Apply range adjustment
df[['range1', 'range2']] = df.apply(lambda row: adjust_range(row['margin']), axis=1, result_type='expand')

# Correct the grouping and summation for margin values
grouped = df.groupby(['tenure', 'range1', 'range2', 'CCY']).agg({'notional': 'sum'}).reset_index()

# Pivot with additional 'tenure' index
pivot_table = grouped.pivot_table(index=['tenure', 'range1', 'range2'], columns='CCY', values='notional', fill_value=0)

# Calculate the 'grand total' across currencies for each row
pivot_table['grand total'] = pivot_table.sum(axis=1)

# Convert the MultiIndex into columns to make it compatible with Dash DataTable
pivot_table.reset_index(inplace=True)

# Sort the pivot table to ensure the rows are ordered correctly
pivot_table.sort_values(by=['tenure', 'range1', 'range2'], inplace=True)

# If needed, you can write this to an Excel file
pivot_table.to_excel("pivot_table_by_tenure.xlsx", index=False)

# Print the pivot table
print(pivot_table)