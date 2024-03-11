import pandas as pd
import numpy as np

# Sample data frame
df = pd.DataFrame({
    'A': [1, 2, 3, 4, 5],
    'B': [6, 7, 8, 9, 10],
    'C': [11, 12, 13, 14, 15],
    'Margin1': [20, 25, 30, 35, 40],
    'Margin2': [15, 20, 25, 30, 35],
    'MarginDelta': [5, 5, 5, 5, 5]
})

# Function to calculate margin delta parameters
def calculate_margin_delta_parameters(x):
    if x < 0:
        return np.floor(x / 5) * 5
    else:
        return np.ceil(x / 5) * 5

# Apply the function to the MarginDelta column
df['margin_delta_parameters'] = df['MarginDelta'].apply(calculate_margin_delta_parameters)

# Create a new data frame to store the counts
categories = ['-10-'] + [f'{i} to {i+5}' for i in range(-10, 50, 5)] + ['50+']
new_df = pd.DataFrame(index=categories, columns=['Count'])

# Initialize counts to 0
new_df['Count'] = 0

# Function to categorize the margin delta parameters
def categorize_margin_delta(x):
    if x < -10:
        return '-10-'
    elif x > 50:
        return '50+'
    else:
        for i in range(-10, 50, 5):
            if i <= x < i + 5:
                return f'{i} to {i+5}'

# Apply the function and count the occurrences
df['Category'] = df['margin_delta_parameters'].apply(categorize_margin_delta)
new_df['Count'] = df['Category'].value_counts()

print(df)
print(new_df)