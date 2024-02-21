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
        dcc.Checklist(
            id='show-delta-toggle',
            options=[{'label': 'Show Delta', 'value': 'show_delta'}],
            value=[],
            inline=True
        ),
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
    Input('right-dropdown', 'value'),
    Input('show-delta-toggle', 'value')
)
def update_data_frames(left_file, right_file, show_delta):
    if left_file and right_file:
        left_df = pd.read_excel(os.path.join(excel_dir, left_file))
        right_df = pd.read_excel(os.path.join(excel_dir, right_file))

        non_string_columns = [col for col in left_df.columns if left_df[col].dtype != object]

        if 'show_delta' in show_delta:
            delta_df = right_df[non_string_columns] - left_df[non_string_columns]
            right_df_display = right_df.copy()
            right_df_display.update(delta_df)
            return html.Pre(left_df.to_string()), html.Pre(right_df_display.to_string())
        return html.Pre(left_df.to_string()), html.Pre(right_df.to_string())
    return 'Select a file on the left', 'Select a file on the right'

# Add callback for sheet selection buttons

if __name__ == '__main__':
    app.run_server(debug=True)