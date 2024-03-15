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

# Function to map margin to range1 and range2
def map_margin_to_range(margin):
    if margin < -10:
        return '<-10', '-10'
    elif margin >= 30:
        return '30', '30+'
    else:
        range1 = margin - (margin % 5)
        range2 = range1 + 5
        return str(range1), str(range2)

# Map the margin to range1 and range2 in the dataframe
df['range1'], df['range2'] = zip(*df['margin'].map(map_margin_to_range))

# Initialize the Dash app
app = Dash(__name__)

# Define the summary DataFrame
summary_df = df.groupby('tenure').agg({'notional': 'sum'}).reset_index()
summary_df.columns = ['Tenure', 'Grand Total']

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

# Callback for updating the table
@app.callback(
    Output('table-container', 'children'),
    [Input('table', 'active_cell')],
    [State('table', 'data')]
)
def display_click_data(active_cell, data):
    if active_cell and 'Tenure' in data[0]:
        tenure = data[active_cell['row']]['Tenure']
        # Filter the DataFrame for the selected tenure and compute the totals
        filtered_df = df[df['tenure'] == tenure]
        ranges_df = filtered_df.groupby(['range1', 'range2', 'CCY']).agg({'notional': 'sum'}).reset_index()
        ranges_df['grand total'] = ranges_df.groupby(['range1', 'range2'])['notional'].transform('sum')
        
        # Format the detailed DataFrame for display
        detailed_table = ranges_df.pivot(index=['range1', 'range2'], columns='CCY', values='notional').fillna(0)
        detailed_table['grand total'] = ranges_df['grand total']
        
        return dash_table.DataTable(
            data=detailed_table.reset_index().to_dict('records'),
            columns=[{"name": i, "id": i} for i in detailed_table.reset_index().columns]
        )
    return "Click on a Tenure cell to view detailed information."

if __name__ == '__main__':
    app.run_server(debug=True)