import pandas as pd

# Creating the DataFrame with the provided data
data = [
    ['itr1', 'ON', 'Jan', 0.02],
    ['itr1', '3m', 'Jan', 0.023],
    ['itr1', '6m', 'Jan', 0.024],
    ['itr1', '1yr', 'Jan', 0.019],
    ['itr2', 'ON', 'Jan', 0.021],
    ['itr2', '3m', 'Jan', 0.028],
    ['itr2', '6m', 'Jan', 0.024],
    ['itr2', '1yr', 'Jan', 0.028],
    ['itr1', 'ON', 'Feb', 0.02],
    ['itr1', '3m', 'Feb', 0.023],
    ['itr1', '6m', 'Feb', 0.024],
    ['itr1', '1yr', 'Feb', 0.019],
    ['itr2', 'ON', 'Feb', 0.021],
    ['itr2', '3m', 'Feb', 0.028],
    ['itr2', '6m', 'Feb', 0.024],
    ['itr2', '1yr', 'Feb', 0.028]
]

columns = ['curve_name', 'period', 'ref_value', 'value']

df = pd.DataFrame(data, columns=columns)
df.head()  # Display the first few rows of the DataFrame to confirm its creation
