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

# Compress the pivot table
compressed_pivot_table = pivot_table.copy()
below_min = compressed_pivot_table.loc[(compressed_pivot_table.index.get_level_values('range2').astype(int) < range_min)].sum()
above_max = compressed_pivot_table.loc[(compressed_pivot_table.index.get_level_values('range1').astype(int) > range_max)].sum()
compressed_pivot_table = compressed_pivot_table[(compressed_pivot_table.index.get_level_values('range1').astype(int) >= range_min) & (compressed_pivot_table.index.get_level_values('range2').astype(int) <= range_max)]
compressed_pivot_table.loc[('< ' + str(range_min), '< ' + str(range_min))] = below_min
compressed_pivot_table.loc[('> ' + str(range_max), '> ' + str(range_max))] = above_max

print(compressed_pivot_table)