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

print(pivot_table)