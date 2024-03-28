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
    [Input('overlay', 'n_clicks')],
    [State('table', 'selected_cells')]
)
def deselect_cells(n_clicks, selected_cells):
    # Check if the callback was triggered by a click on the overlay
    if callback_context.triggered[0]['prop_id'] == 'overlay.n_clicks':
        return []
    return dash.no_update

if __name__ == '__main__':
    app.run_server(debug=True)