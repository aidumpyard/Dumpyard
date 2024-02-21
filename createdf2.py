import dash
from dash import html
import dash_table
import pandas as pd

# Read the entire Excel file
excel_data = pd.read_excel('your_excel_file.xlsx', header=None)

# Extract the three dataframes based on the row and column indices
df1 = excel_data.iloc[3:12, 0:4]
df1.columns = df1.iloc[0]
df1 = df1.drop(df1.index[0])

df2 = excel_data.iloc[17:52, 10:12]
df2.columns = df2.iloc[0]
df2 = df2.drop(df2.index[0])

df3 = excel_data.iloc[3:12, 10:12]
df3.columns = df3.iloc[0]
df3 = df