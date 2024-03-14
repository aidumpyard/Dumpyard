import pandas as pd

# Adjusted sample data
data = {
    'margin': [-20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40],
    'CCY': ['USD', 'USD', 'USD', 'USD', 'EUR', 'EUR', 'USD', 'EUR', 'USD', 'USD', 'USD', 'USD', 'USD'],
    'notional': [200, 200, 200, 200, 100, 300, 400, 500, 600, 600, 600, 600, 600]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Define custom function to set the range values
def set_range(value, lower_bound, upper_bound):
    if value < lower_bound:
        return f'<{lower_bound}'
    elif value >= upper_bound:
        return f'{upper_bound}+'
    else:
        return value

# Apply custom function to 'margin' to create 'range1' and 'range2'
df['range1'] = df['margin'].apply(lambda x: set_range(x, -10, 30) if x != 30 else 30)
df['range2'] = df['margin'].apply(lambda x: set_range(x + 5, -10, 30) if x != 30 else '30+')

# Create the pivot table
pivot_table = df.pivot_table(index=['range1', 'range2'], columns='CCY', values='notional', aggfunc='sum', fill_value=0)

# Reset index if you want 'range1' and 'range2' as columns
pivot_table.reset_index(inplace=True)

# Display the pivot table
print(pivot_table)