import os
from dash import Dash, html, dcc, Input, Output
from dash.exceptions import PreventUpdate
from dash_bootstrap_components import Container, Row, Col, Dropdown, ButtonGroup, Button, FormGroup, RadioItems
import pandas as pd

# Sample directory containing Excel files
excel_dir = "path_to_your_directory"

# Function to list all Excel files in a directory
def list_excel_files(directory):
    files = os.listdir(directory)
    excel_files = [file for file in files if file.endswith(".xlsx")]
    return excel_files

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'])

# App layout
app.layout = Container([
    Row([
        Col([
            html.H3("Select Excel File"),
            Dropdown(
                id='excel-dropdown',
                options=[{'label': file, 'value': file} for file in list_excel_files(excel_dir)],
                placeholder="Select an Excel file"
            ),
            html.Div(id='output-file')
        ]),
        Col([
            html.H3("Select Sheet"),
            RadioItems(
                id='sheet-radio',
                options=[],
                value=''
            ),
            html.Div(id='output-sheet')
        ]),
        Col([
            html.H3("Display Differences"),
            RadioItems(
                id='diff-radio',
                options=[
                    {'label': 'Show Differences', 'value': 'show'},
                    {'label': 'Show As Is', 'value': 'asis'}
                ],
                value='show'
            ),
            html.Div(id='output-diff')
        ]),
    ])
])

# Callback to update the sheet options based on the selected Excel file
@app.callback(
    Output('sheet-radio', 'options'),
    Output('sheet-radio', 'value'),
    Input('excel-dropdown', 'value')
)
def update_sheet_options(selected_file):
    if not selected_file:
        raise PreventUpdate

    excel_file_path = os.path.join(excel_dir, selected_file)
    sheets = pd.ExcelFile(excel_file_path).sheet_names

    return [{'label': sheet, 'value': sheet} for sheet in sheets], sheets[0]

# Callback to display the selected Excel file
@app.callback(
    Output('output-file', 'children'),
    Output('output-sheet', 'children'),
    Output('output-diff', 'children'),
    Input('excel-dropdown', 'value'),
    Input('sheet-radio', 'value'),
    Input('diff-radio', 'value')
)
def display_file(selected_file, selected_sheet, diff_radio):
    if not selected_file or not selected_sheet:
        raise PreventUpdate

    excel_file_path = os.path.join(excel_dir, selected_file)
    df = pd.read_excel(excel_file_path, sheet_name=selected_sheet)

    # Display differences or the entire sheet based on the radio button selection
    if diff_radio == 'show':
        # Assuming df1 is the first selected Excel file and df2 is the second
        # df_diff = df1.compare(df2)
        # display = df_diff
        display = html.Pre("Differences will be displayed here.")
    else:
        display = html.Table([
            html.Thead(
                html.Tr([html.Th(col) for col in df.columns])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(df.iloc[i][col]) for col in df.columns
                ]) for i in range(len(df))
            ])
        ])

    return f"Selected Excel file: {selected_file}", f"Selected Sheet: {selected_sheet}", display

if __name__ == '__main__':
    app.run_server(debug=True)