import pandas as pd

# Example DataFrame
data = {
    'period': ['2021', '2022'],
    'Iyer': [100, 200],
    'Dalai': [150, 250]
}

df = pd.DataFrame(data)

# Transforming the DataFrame
melted_df = pd.melt(df, id_vars=['period'], var_name='title', value_name='value')

print(melted_df)