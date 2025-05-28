import dash
from dash import html, dcc, Input, Output, State, dash_table
import base64
import os
import pandas as pd
from datetime import datetime

from config.config_loader import Config
from core.business_flow import business_flow
from core.uploadfile_dataframe import uploadfile_dataframe
from core.enrichment import enrich_transposed_data
from utils.update_generic_enriched_file import update_monthly_generic_enriched
from utils.file_saver_utils import save_with_iteration
from utils.enhanced_upload_ledger_utils import load_upload_ledger_from_config

app = dash.Dash(__name__)
server = app.server

config = Config('data/FTP_Config.xlsx')
file_type_options = [{'label': ft, 'value': ft} for ft in config.get_available_filetypes()]
planning_months = [f"{m}'25" for m in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']]
ledger_file = 'uploader_ledger.xlsx'

app.layout = html.Div([
    html.H1("Forecast File Uploader - Dash Interface"),
    html.Label("Select File Type:"),
    dcc.Dropdown(id='file-type-dropdown', options=file_type_options, value=file_type_options[0]['value'] if file_type_options else None),
    html.Label("Select Planning Month:"),
    dcc.Dropdown(id='planning-month-dropdown', options=[{'label': m, 'value': m} for m in planning_months], value=planning_months[0]),
    html.Label("Enter Username:"),
    dcc.Input(id='uploaded-by', type='text', value='admin'),
    html.Br(), html.Br(),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', html.A('Select a File')]),
        style={'width': '100%', 'height': '80px', 'lineHeight': '80px', 'borderWidth': '1px',
               'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center'},
        multiple=False
    ),
    html.Div(id='upload-status'),
    html.Hr(),
    html.H4("Upload Ledger"),
    dash_table.DataTable(
        id='upload-table',
        columns=[
            {'name': 'File Type', 'id': 'file_type'},
            {'name': 'Iteration No', 'id': 'iteration'},
            {'name': 'Status', 'id': 'upload_status'}
        ],
        data=[],
        row_selectable='single',
        style_table={'overflowX': 'auto'}
    ),
    html.Div(id='download-link'),
    html.Div(id='monthly-generic-download')
])

@app.callback(
    [Output('upload-status', 'children'), Output('upload-table', 'data')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'), State('file-type-dropdown', 'value'),
     State('planning-month-dropdown', 'value'), State('uploaded-by', 'value')]
)
def handle_upload(contents, filename, filetype, planning_month, uploaded_by):
    if contents is None:
        return "", []

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    temp_path = f"temp_upload.xlsx"
    with open(temp_path, "wb") as f:
        f.write(decoded)

    flow = business_flow(planning_month)
    file_category = next((k for k in flow.file_status_dict if filetype.lower().startswith(k)), 'forecast')

    updf = uploadfile_dataframe(temp_path, filetype, "Forecast", planning_month, flow, config)
    df_transposed = updf.load_and_transform()
    df_enriched = enrich_transposed_data(df_transposed, config)

    iteration = flow.get_next_iteration(file_category, filetype)
    enriched_path = save_with_iteration(df_enriched, filetype, iteration, planning_month, status="Success")
    flow.update_file_status(file_category, filetype, os.path.basename(enriched_path), uploaded_by, "Success", iteration)
    update_monthly_generic_enriched(df_enriched, filetype, planning_month, config)

    df_ledger = load_upload_ledger_from_config(config, planning_month)
    return f"Uploaded and processed: {filename}", df_ledger.to_dict('records')

@app.callback(
    Output('download-link', 'children'),
    [Input('upload-table', 'selected_rows')],
    [State('upload-table', 'data'), State('planning-month-dropdown', 'value')]
)
def download_file(selected_rows, table_data, planning_month):
    if selected_rows and table_data:
        row = table_data[selected_rows[0]]
        if row['upload_status'].lower() == 'success':
            year = f"20{planning_month[-2:]}"
            month_map = {'Jan': 'January', 'Feb': 'February', 'Mar': 'March', 'Apr': 'April',
                         'May': 'May', 'Jun': 'June', 'Jul': 'July', 'Aug': 'August',
                         'Sep': 'September', 'Oct': 'October', 'Nov': 'November', 'Dec': 'December'}
            month = month_map.get(planning_month[:3], planning_month[:3])
            enriched_file = f"{row['file_type']}_v{row['iteration']}.xlsx"
            path = os.path.join('output', year, month, enriched_file)
            if os.path.exists(path):
                return html.A("Download File", href=f"/download/{year}/{month}/{enriched_file}", target="_blank")
    return ""

@app.callback(
    Output('monthly-generic-download', 'children'),
    [Input('upload-table', 'data')],
    [State('planning-month-dropdown', 'value')]
)
def show_monthly_enriched_download(data, planning_month):
    if not data:
        return ""
    month_file = f"generic_enriched_{planning_month.replace("'", '')}.xlsx"
    path = os.path.join('output', month_file)
    if os.path.exists(path):
        return html.A("Download Monthly Generic Enriched File", href=f"/download/{month_file}", target="_blank")
    return ""

if __name__ == '__main__':
    app.run_server(debug=True)
