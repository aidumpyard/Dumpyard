import pandas as pd

# Sample DataFrame
data = {
    'col1': ['A', 'A', 'B', 'B', 'C', 'C'],
    'col2': [1, 2, 1, 2, 1, 2],
    'col3': [10, 20, 30, 40, 50, 60],
    'col4': [100, 200, 300, 400, 500, 600],
    'col5': [1000, 2000, 3000, 4000, 5000, 6000],
    'col6': [10000, 20000, 30000, 40000, 50000, 60000]
}
df = pd.DataFrame(data)

# List of pairs provided by the user
pairs = [('A', 1), ('B', 2)]

# Split the DataFrame based on the pairs
dfs = [df[(df['col1'] == pair[0]) & (df['col2'] == pair[1])] for pair in pairs]

# Print the separate DataFrames
for i, df in enumerate(dfs):
    print(f"DataFrame {i + 1}:\n{df}\n")