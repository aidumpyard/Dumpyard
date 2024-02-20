import os
import pandas as pd
import dash
from dash import dcc, html
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
            placeholder="Select an Excel file (Right)",
        ),
        html.Button('Show Delta', id='show-delta-btn', n_clicks=0),
        dcc.Dropdown(id='common-columns-dropdown', multi=True),
        html.Div(id='sheet-selection-buttons'),
    ], style={'width': '49%', 'display': 'inline-block'}),

    html.Div(id='left-output', style={'width': '49%', 'display': 'inline-block'}),
    html.Div(id='right-output', style={'width': '49%', 'display': 'inline-block'}),
])

@app.callback(
    Output('right-dropdown', 'options'),
    Input('left-dropdown', 'value')
)
def update_right_dropdown(selected_left_file):
    if selected_left_file:
        return [{'label': file, 'value': file} for file in excel_files if file != selected_left_file]
    return [{'label': file, 'value': file} for file in excel_files]

@app.callback(
    Output('left-output', 'children'),
    Output('right-output', 'children'),
    Input('left-dropdown', 'value'),
    Input('right-dropdown', 'value')
)
def update_data_frames(left_file, right_file):
    if left_file and right_file:
        left_df = pd.read_excel(os.path.join(excel_dir, left_file))
        right_df = pd.read_excel(os.path.join(excel_dir, right_file))
        return html.Pre(left_df.to_string()), html.Pre(right_df.to_string())
    return 'Select a file on the left', 'Select a file on the right'

# Add callbacks for Show Delta, common columns dropdown, and sheet selection buttons

if __name__ == '__main__':
    app.run_server(debug=True)