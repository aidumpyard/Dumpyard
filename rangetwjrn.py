import pandas as pd

# Sample data
data = {
    'margin': [-30, -25, -20, 10, 15, 20],
    'CCY': ['EUR', 'USD', 'EUR', 'USD', 'EUR', 'USD'],
    'notional': [100, 200, 300, 400, 500, 600]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Define the ranges
df['range1'] = df['margin'] - 5
df['range2'] = df['margin']

# Create a pivot table
pivot_table = df.pivot_table(index=['range1', 'range2'], columns='CCY', values='notional', aggfunc='sum', fill_value=0, margins=True, margins_name='grand total')

# Calculate cumulative sums
pivot_table['Cumulative EUR'] = pivot_table[('EUR')].cumsum()
pivot_table['Cumulative USD'] = pivot_table[('USD')].cumsum()
pivot_table['Cumulative Total'] = pivot_table[('grand total')].cumsum()

# Define the compression range
range_min = -20
range_max = 10

# Function to compress ranges
def compress_ranges(row_index):
    range1, range2 = row_index
    if isinstance(range1, str) or isinstance(range2, str):
        return (range1, range2)
    elif range2 < range_min:
        return (f'< {range_min}', f'< {range_min}')
    elif range1 > range_max:
        return (f'> {range_max}', f'> {range_max}')
    else:
        return (range1, range2)

# Compress the pivot table
compressed_pivot_table = pivot_table.groupby(compress_ranges).sum()

print(compressed_pivot_table)