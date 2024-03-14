import pandas as pd

# Adjusted sample data
data = {
    'margin': [-20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45],
    'CCY': ['USD', 'USD', 'USD', 'USD', 'EUR', 'EUR', 'USD', 'EUR', 'USD', 'USD', 'USD', 'USD', 'USD', 'USD'],
    'notional': [200, 200, 200, 200, 100, 300, 400, 500, 600, 600, 600, 600, 600, 600]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Adjust the ranges based on the conditions
def adjust_ranges(row):
    if row['margin'] < -10:
        return '<-10', '-10'
    elif row['margin'] > 30:
        return '30', '30+'
    else:
        return row['margin'] - (row['margin'] % 5), row['margin'] + 5 - (row['margin'] % 5)

# Apply the function to adjust ranges
df[['range1', 'range2']] = df.apply(adjust_ranges, axis=1, result_type='expand')

# Group by the new ranges before pivot to sum notional values outside the bounds
grouped = df.groupby(['range1', 'range2', 'CCY']).agg({'notional': 'sum'}).reset_index()

# Now create the pivot table
pivot_table = grouped.pivot_table(index=['range1', 'range2'], columns='CCY', values='notional', aggfunc='sum', fill_value=0)

# Add a grand total by summing across the columns
pivot_table['grand total'] = pivot_table.sum(axis=1)

# Sort the table based on custom key
sorter = {'<-10': -float('inf'), '30+': float('inf')}
pivot_table = pivot_table.sort_index(key=lambda x: x.map(lambda y: sorter.get(y, y)))

# Print the pivot table
print(pivot_table)