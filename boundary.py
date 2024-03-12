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

# Compress the ranges into the specified boundary
boundary_min = -20
boundary_max = 10
df['compressed_range1'] = df['range1'].apply(lambda x: '<' + str(boundary_min) if x < boundary_min else x)
df['compressed_range2'] = df['range2'].apply(lambda x: '>' + str(boundary_max) if x > boundary_max else x)

# Create a pivot table
pivot_table = df.pivot_table(index=['compressed_range1', 'compressed_range2'], columns='CCY', values='notional', aggfunc='sum', fill_value=0, margins=True, margins_name='grand total')

print(pivot_table)