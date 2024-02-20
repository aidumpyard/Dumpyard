import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import os
import dash_table
directory = 'path/to/your/excel/files'
excel_files = [file for file in os.listdir(directory) if file.endswith('.xlsx')]

app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Dropdown(
        id='left-dropdown',
        options=[{'label': file, 'value': file} for file in excel_files],
        placeholder='Select a file for the left side'
    ),
    dcc.Dropdown(
        id='right-dropdown',
        placeholder='Select a file for the right side'
    ),
    html.Button('Show Difference', id='diff-button', n_clicks=0),
    html.Div([
        dash_table.DataTable(id='left-table', style_table={'width': '50%', 'display': 'inline-block'}),
        dash_table.DataTable(id='right-table', style_table={'width': '50%', 'display': 'inline-block'})
    ])
])



@app.callback(
    Output('right-dropdown', 'options'),
    Input('left-dropdown', 'value')
)
def update_right_dropdown(selected_file):
    if selected_file:
        return [{'label': file, 'value': file} for file in excel_files if file != selected_file]
    return []

@app.callback(
    Output('left-table', 'data'),
    Output('left-table', 'columns'),
    Input('left-dropdown', 'value')
)
def update_left_table(selected_file):
    if selected_file:
        df = pd.read_excel(os.path.join(directory, selected_file))
        return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]
    return [], []

@app.callback(
    Output('right-table', 'data'),
    Output('right-table', 'columns'),
    Input('right-dropdown', 'value'),
    State('left-dropdown', 'value'),
    State('diff-button', 'n_clicks')
)
def update_right_table(selected_file, left_file, n_clicks):
    if selected_file:
        right_df = pd.read_excel(os.path.join(directory, selected_file))
        if n_clicks > 0 and left_file:
            left_df = pd.read_excel(os.path.join(directory, left_file))
            diff_df = right_df.copy()
            diff_df['value1'] = right_df['value1'] - left_df['value1']
            diff_df['value2'] = right_df['value2'] - left_df['value2']
            diff_df['color1'] = ['green' if val > 0 else 'red' if val < 0 else '-' for val in diff_df['value1']]
            diff_df['color2'] = ['green' if val > 0 else 'red' if val < 0 else '-' for val in diff_df['value2']]
            return diff_df.to_dict('records'), [{"name": i, "id": i} for i in diff_df.columns]
        return right_df.to_dict('records'), [{"name": i, "id": i} for i in right_df.columns]
    return [], []

if __name__ == '__main__':
    app.run_server(debug=True)












