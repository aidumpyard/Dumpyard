import dash
from dash import Dash, dcc, html, dash_table, Input, Output, State
import pandas as pd

# Adjusted sample data including 'tenure'
data = {
    'tenure': [0] * 13 + [1] * 13,
    'margin': [-20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40] * 2,
    'CCY': ['USD', 'USD', 'USD', 'USD', 'EUR', 'EUR', 'USD', 'EUR', 'USD', 'USD', 'USD', 'USD', 'USD'] * 2,
    'notional': [200, 200, 200, 200, 100, 300, 400, 500, 600, 600, 600, 600, 600] * 2
}

# Create a DataFrame
df = pd.DataFrame(data)

# Define the layout of your Dash app
app = Dash(__name__)

# Set up the summary DataFrame
summary_df = df.groupby('tenure')['notional'].sum().reset_index()
summary_df['range1'] = '<-10'  # This is just a placeholder
summary_df['range2'] = '30+'  # This is just a placeholder
summary_df.rename(columns={'notional': 'grand total'}, inplace=True)

# Add placeholders for 'EUR' and 'USD' columns in the summary
for ccy in ['EUR', 'USD']:
    summary_df[ccy] = df[df['CCY'] == ccy].groupby('tenure')['notional'].sum().reset_index(drop=True)

app.layout = html.Div([
    dash_table.DataTable(
        id='summary-table',
        columns=[{"name": i, "id": i} for i in summary_df.columns],
        data=summary_df.to_dict('records'),
        style_table={'overflowX': 'auto'},
        row_selectable='single',  # Set up row selection
        selected_rows=[]
    ),
    html.Div(id='detail-view')  # Placeholder for detailed view
])

# Define the callback for interactive table update
@app.callback(
    [Output('summary-table', 'data'),
     Output('summary-table', 'selected_rows')],
    [Input('summary-table', 'selected_rows')],
    [State('summary-table', 'data')]
)
def update_table(selected_rows, data):
    # If a row is selected, show detailed view for that tenure
    if selected_rows:
        selected_tenure = selected_rows[0]
        detail_df = df[df['tenure'] == selected_tenure]
        return detail_df.to_dict('records'), selected_rows
    # If no row is selected, return to summary view
    else:
        return summary_df.to_dict('records'), []

if __name__ == '__main__':
    app.run_server(debug=True)