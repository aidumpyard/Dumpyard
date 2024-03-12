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

# Define the compression range
range_min = -20
range_max = 10

# Compress the data
compressed_data = []
below_min = {'range1': f'< {range_min}', 'range2': f'< {range_min}', 'CCY': 'EUR', 'notional': 0}
above_max = {'range1': f'> {range_max}', 'range2': f'> {range_max}', 'CCY': 'EUR', 'notional': 0}
for _, row in df.iterrows():
    if row['range1'] < range_min:
        below_min['notional'] += row['notional']
    elif row['range2'] > range_max:
        above_max['notional'] += row['notional']
    else:
        compressed_data.append(row.to_dict())

compressed_data.append(below_min)
compressed_data.append(above_max)

# Create a new DataFrame with the compressed data
compressed_df = pd.DataFrame(compressed_data)

# Create a pivot table
pivot_table = compressed_df.pivot_table(index=['range1', 'range2'], columns='CCY', values='notional', aggfunc='sum', fill_value=0, margins=True, margins_name='grand total')

# Calculate cumulative sums
pivot_table['Cumulative EUR'] = pivot_table[('EUR')].cumsum()
pivot_table['Cumulative USD'] = pivot_table[('USD')].cumsum()
pivot_table['Cumulative Total'] = pivot_table[('grand total')].cumsum()

print(pivot_table)