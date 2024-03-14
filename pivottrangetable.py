import pandas as pd
import dash
from dash import dcc, html
import dash_table

# Sample data
data = {
    'margin': [-20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40],
    'CCY': ['USD', 'USD', 'USD', 'USD', 'EUR', 'EUR', 'USD', 'EUR', 'USD', 'USD', 'USD', 'USD', 'USD'],
    'notional': [200, 200, 200, 200, 100, 300, 400, 500, 600, 600, 600, 600, 600]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Define the ranges with limits
df['range1'] = df['margin'].apply(lambda x: '<-10' if x < -10 else x - 5)
df['range2'] = df['margin'].apply(lambda x: '30+' if x > 30 else x if x == 30 else x + 5)

# Create a pivot table
pivot_table = df.pivot_table(index=['range1', 'range2'], columns='CCY', values='notional', aggfunc='sum', fill_value=0, margins=True, margins_name='grand total')

# Calculate cumulative sums
pivot_table['Cumulative EUR'] = pivot_table[('EUR')].cumsum()
pivot_table['Cumulative USD'] = pivot_table[('USD')].cumsum()
pivot_table['Cumulative Total'] = pivot_table[('grand total')].cumsum()

# Write the pivot table to an Excel file
pivot_table.to_excel("pivot_table_with_cumsum.xlsx")

# Create a Dash app to display the pivot table
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Pivot Table with Cumulative Sums"),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in pivot_table.columns],
        data=pivot_table.to_dict('records'),
        style_table={'overflowX': 'auto'},
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)