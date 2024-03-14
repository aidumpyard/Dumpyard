import pandas as pd
import dash
from dash import dcc, html
import dash_table

# Sample data with an additional 'tenure' column
data = {
    'margin': [-20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40] * 2,
    'CCY': ['USD', 'USD', 'USD', 'USD', 'EUR', 'EUR', 'USD', 'EUR', 'USD', 'USD', 'USD', 'USD', 'USD'] * 2,
    'notional': [200, 200, 200, 200, 100, 300, 400, 500, 600, 600, 600, 600, 600] * 2,
    'tenure': ['1Y'] * 13 + ['2Y'] * 13
}

# Create a DataFrame
df = pd.DataFrame(data)

# Define the ranges with limits
df['range1'] = df['margin'].apply(lambda x: '<-10' if x < -10 else x - 5)
df['range2'] = df['margin'].apply(lambda x: '30+' if x > 30 else x if x == 30 else x + 5)

# Create a pivot table for each unique tenure value
pivot_tables = {}
for tenure in df['tenure'].unique():
    tenure_df = df[df['tenure'] == tenure]
    pivot_table = tenure_df.pivot_table(index=['range1', 'range2'], columns='CCY', values='notional', aggfunc='sum', fill_value=0, margins=True, margins_name='grand total')
    
    # Calculate cumulative sums
    pivot_table['Cumulative EUR'] = pivot_table[('EUR')].cumsum()
    pivot_table['Cumulative USD'] = pivot_table[('USD')].cumsum()
    pivot_table['Cumulative Total'] = pivot_table[('grand total')].cumsum()
    
    pivot_tables[tenure] = pivot_table

# Write the pivot tables to an Excel file
with pd.ExcelWriter("pivot_tables_by_tenure.xlsx") as writer:
    for tenure, pivot_table in pivot_tables.items():
        pivot_table.to_excel(writer, sheet_name=f"Tenure {tenure}")

# Create a Dash app to display the pivot tables
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Pivot Tables by Tenure"),
    html.Div([
        html.H2(f"Tenure: {tenure}"),
        dash_table.DataTable(
            id=f'table-{tenure}',
            columns=[{"name": i, "id": i} for i in pivot_table.columns],
            data=pivot_table.to_dict('records'),
            style_table={'overflowX': 'auto'},
        )
        for tenure, pivot_table in pivot_tables.items()
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)