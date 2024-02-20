import os
import pandas as pd
import dash
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

# Path to the directory containing Excel files
excel_dir = "/path/to/your/excel/files"

# List all Excel files in the directory
excel_files = [f for f in os.listdir(excel_dir) if f.endswith(".xlsx")]

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='left-dropdown',
            options=[{'label': file, 'value': file} for file in excel_files],
            placeholder="Select an Excel file (Left)",
        ),
    ], style={'width': '49%', 'display': 'inline-block'}),

    html.Div([
        dcc.Dropdown(
            id='right-dropdown',
            options=[{'label': file, 'value': file} for file in excel_files],
            placeholder="Select an Excel file (Right)",
        ),
        html.Button('Show Delta', id='show-delta-btn', n_clicks=0),
        # Placeholder for common columns dropdown
        dcc.Dropdown(id='common-columns-dropdown', multi=True),
        # Placeholder for sheet selection buttons
        html.Div(id='sheet-selection-buttons'),
    ], style={'width': '49%', 'display': 'inline-block'}),

    html.Div(id='delta-output')
])

@app.callback(
    Output('delta-output', 'children'),
    Input('show-delta-btn', 'n_clicks'),
    Input('left-dropdown', 'value'),
    Input('right-dropdown', 'value'),
    prevent_initial_call=True
)
def show_delta(n_clicks, left_file, right_file):
    if n_clicks == 0:
        raise PreventUpdate

    # Load the selected Excel files
    left_df = pd.read_excel(os.path.join(excel_dir, left_file))
    right_df = pd.read_excel(os.path.join(excel_dir, right_file))

    # Calculate the delta values
    delta_df = right_df - left_df

    return html.Pre(delta_df.to_string())

if __name__ == '__main__':
    app.run_server(debug=True)
    