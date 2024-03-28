import dash
from dash import html, dcc, Input, Output, State, dash_table, callback_context
import pandas as pd

# Sample DataFrame
df = pd.DataFrame({
    "A": [1, 2, 3, 4],
    "B": [5, 6, 7, 8]
})

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(id='overlay', style={'position': 'fixed', 'top': 0, 'left': 0, 'height': '100%', 'width': '100%', 'zIndex': -1}),
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
    [Input('overlay', 'n_clicks'), Input('table', 'active_cell')],
    prevent_initial_call=True
)
def deselect_cells(n_clicks, active_cell):
    ctx = callback_context
    if ctx.triggered:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger_id == 'overlay':
            return []
    return dash.no_update

if __name__ == '__main__':
    app.run_server(debug=True)