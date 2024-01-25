import pandas as pd
import plotly.express as px
import calendar

# Sample DataFrame
# Replace this with your actual DataFrame
data = {
    'series': ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D'],
    'month': ['Jan', 'Feb', 'Jul', 'Aug', 'Jan', 'Feb', 'Aug', 'Sep'],
    'output': [10, 15, 20, 25, 30, 35, 40, 45]
}
df = pd.DataFrame(data)

# Convert 'month' to categorical type with proper order
month_order = list(calendar.month_abbr)[1:]
df['month'] = pd.Categorical(df['month'], categories=month_order, ordered=True)

# Sort the DataFrame
df.sort_values(by=['series', 'month'], inplace=True)

# Plotting with Plotly
fig = px.line(df, x='month', y='output', color='series', 
              labels={'output': 'Output', 'month': 'Month'}, 
              title='Monthly Output by Series')

fig.show()