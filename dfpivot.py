import pandas as pd

# Sample data
data = {
    'Column1': ['A', 'B', 'A', 'B', 'A', 'B'],
    'CCY': ['USD', 'EUR', 'USD', 'EUR', 'GBP', 'GBP'],
    'Notional': [100, 200, 300, 400, 500, 600]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Create a pivot table
pivot_table = df.pivot_table(
    index='Column1',
    columns='CCY',
    values='Notional',
    aggfunc='sum',
    fill_value=0  # Fill missing values with 0
)

# Display the pivot table
print(pivot_table)