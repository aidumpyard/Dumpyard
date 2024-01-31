import pandas as pd

# Example DataFrame
data = {'date_str': ['Feb-23', 'Jun-23', 'Jan-23', 'Mar-23']}
df = pd.DataFrame(data)

# Convert the string dates to datetime objects
df['date_dt'] = pd.to_datetime(df['date_str'], format='%b-%y')

# Sort the DataFrame by the datetime column
df_sorted = df.sort_values(by='date_dt')

print(df_sorted)