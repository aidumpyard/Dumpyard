import dash
from dash import Dash, dcc, html, dash_table, Input, Output
import pandas as pd

# Sample data
data = {
    'tenure': [0] * 13 + [1] * 13,
    'margin': [-20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40] * 2,
    'CCY': ['USD', 'USD', 'USD', 'USD', 'EUR', 'EUR', 'USD', 'EUR', 'USD', 'USD', 'USD', 'USD', 'USD'] * 2,
    'notional': [200, 200, 200, 200, 100, 300, 400, 500, 600, 600, 600, 600, 600] * 2
}
df = pd.DataFrame(data)

# Define the layout of your Dash app
app = Dash(__name__)

# Define the summary DataFrame
def create_summary():
    summary = df.groupby(['tenure']).agg({'notional': 'sum'}).reset_index()
    summary.columns = ['Tenure', 'Grand Total']
    return summary

summary_df = create_summary()

# Set up the Dash DataTable
app.layout = html.Div([
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in summary_df.columns],
        data=summary_df.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_data_conditional=[
            {'if': {'column_id': 'Tenure'},
             'cursor': 'pointer'}
        ],
    ),
    html.Div(id='table-container')
])

# Callback for updating table
@app.callback(
    Output('table-container', 'children'),
    [Input('table', 'active_cell')],
    [State('table', 'data')]
)
def display_click_data(active_cell, data):
    if active_cell:
        tenure = data[active_cell['row']]['Tenure']
        detailed_df = df[df['tenure'] == tenure]
        # Create a pivot table with the detailed data
        pivot = detailed_df.pivot_table(index=['tenure', 'margin'], columns='CCY', values='notional', aggfunc='sum', fill_value=0, margins=True, margins_name='Total')
        return dash_table.DataTable(
            data=pivot.reset_index().to_dict('records'),
            columns=[{"name": i, "id": i} for i in pivot.reset_index().columns]
        )
    return "Click on a Tenure cell to view detailed information."

if __name__ == '__main__':
    app.run_server(debug=True)