import pandas as pd

# Adjusted sample data
data = {
    'margin': [-20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40],
    'CCY': ['USD', 'USD', 'USD', 'USD', 'EUR', 'EUR', 'USD', 'EUR', 'USD', 'USD', 'USD', 'USD', 'USD'],
    'notional': [200, 200, 200, 200, 100, 300, 400, 500, 600, 600, 600, 600, 600]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Define the ranges with limits
df['range1'] = df['margin'].apply(lambda x: '<-10' if x < -10 else x - 5)
df['range2'] = df['margin'].apply(lambda x: '30+' if x > 30 else x if x == 30 else x + 5)

# Create a pivot table
pivot_table = df.pivot_table(index=['range1', 'range2'], columns='CCY', values='notional', aggfunc='sum', fill_value=0, margins=True, margins_name='grand total')

# Drop the 'grand total' row and column for display
display_table = pivot_table.drop('grand total', level=0, axis=0).drop('grand total', axis=1)

print(display_table)