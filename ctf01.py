import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import os

# Get all Excel files from a directory
directory = 'path/to/your/excel/files'
excel_files = [f for f in os.listdir(directory) if f.endswith('.xlsx') or f.endswith('.xls')]

# Initialize the Dash app
app = dash.Dash(__name__)

# Set up the app layout
app.layout = html.Div([
    dcc.Dropdown(
        id='file-dropdown',
        options=[{'label': f, 'value': f} for f in excel_files],
        placeholder='Select an Excel file'
    ),
    html.Div(id='dataframes-container'),
    dcc.Dropdown(
        id='second-file-dropdown',
        placeholder='Select another Excel file'
    ),
    html.Div(id='second-dataframes-container')
])

# Callback to update dataframes based on the selected file
@app.callback(
    Output('dataframes-container', 'children'),
    Input('file-dropdown', 'value')
)
def update_dataframes(selected_file):
    if selected_file is not None:
        df1 = pd.read_excel(os.path.join(directory, selected_file), sheet_name=0)
        df2 = pd.read_excel(os.path.join(directory, selected_file), sheet_name=1)
        return [
            html.H5('DataFrame 1'),
            dcc.Graph(figure=df1.to_dict('records')),
            html.H5('DataFrame 2'),
            dcc.Graph(figure=df2.to_dict('records'))
        ]
    return []

# Callback to update the second dropdown and dataframes
@app.callback(
    [Output('second-file-dropdown', 'options'),
     Output('second-dataframes-container', 'children')],
    [Input('file-dropdown', 'value'),
     Input('second-file-dropdown', 'value')]
)
def update_second_dropdown_and_dataframes(selected_file, second_selected_file):
    if selected_file is not None:
        remaining_files = [f for f in excel_files if f != selected_file]
        options = [{'label': f, 'value': f} for f in remaining_files]
        if second_selected_file is not None:
            df3 = pd.read_excel(os.path.join(directory, second_selected_file), sheet_name=0)
            df4 = pd.read_excel(os.path.join(directory, second_selected_file), sheet_name=1)
            dataframes = [
                html.H5('DataFrame 3'),
                dcc.Graph(figure=df3.to_dict('records')),
                html.H5('DataFrame 4'),
                dcc.Graph(figure=df4.to_dict('records'))
            ]
        else:
            dataframes = []
        return options, dataframes
    return [], []

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)