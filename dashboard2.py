import dash
from dash import html, dcc, Input, Output, State, dash_table
import pandas as pd

# Sample DataFrame
df = pd.DataFrame({
    "A": [1, 2, 3, 4],
    "B": [5, 6, 7, 8]
})

app = dash.Dash(__name__)

app.layout = html.Div([
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_data_conditional=[
            {
                'if': {'state': 'selected'},
                'backgroundColor': 'lightblue',
                'border': '1px solid blue'
            }
        ]
    ),
    html.Div(id='output-container')
])

@app.callback(
    Output('table', 'selected_cells'),
    [Input('table', 'active_cell')],
    [State('table', 'selected_cells')]
)
def deselect_cells(active_cell, selected_cells):
    if not active_cell:
        return []
    return dash.no_update

if __name__ == '__main__':
    app.run_server(debug=True)