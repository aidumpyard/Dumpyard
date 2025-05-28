import dash
from dash import html, dcc, Input, Output, State, dash_table
import base64
import io
import os
import pandas as pd
from datetime import datetime

from config.config_loader import Config
from core.business_flow import business_flow
from core.uploadfile_dataframe import uploadfile_dataframe
from core.enrichment import enrich_transposed_data

# Initialize app and config
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
        style={
            'width': '100%',
            'height': '80px',
            'lineHeight': '80px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
        },
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
    html.Div(id='download-link')
])

@app.callback(
    [Output('upload-status', 'children'),
     Output('upload-table', 'data')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'),
     State('file-type-dropdown', 'value'),
     State('planning-month-dropdown', 'value'),
     State('uploaded-by', 'value')]
)
def handle_upload(contents, filename, filetype, planning_month, uploaded_by):
    if contents is None:
        return "", []

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    temp_path = f"output/temp_{filetype}_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    os.makedirs("output", exist_ok=True)

    with open(temp_path, "wb") as f:
        f.write(decoded)

    flow = business_flow(planning_month)
    file_category = None
    for category in flow.file_status_dict:
        if filetype.lower().startswith(category):
            file_category = category
            break
    if not file_category:
        file_category = 'forecast'

    updf = uploadfile_dataframe(temp_path, filetype, "Forecast", planning_month, flow, config)
    df_transposed = updf.load_and_transform()
    df_enriched = enrich_transposed_data(df_transposed, config)

    enriched_file_name = f"enriched_{filetype}_{planning_month.replace("'", '')}.xlsx"
    enriched_file_path = os.path.join("output", enriched_file_name)
    df_enriched.to_excel(enriched_file_path, index=False)

    flow.update_file_status(file_category, filetype, enriched_file_name, uploaded_by, "Success")

    # Read updated ledger
    if os.path.exists(ledger_file):
        xl = pd.ExcelFile(ledger_file)
        df_ledger = xl.parse(planning_month)
        df_ledger = df_ledger[['file_type', 'iteration', 'upload_status']].rename(columns={
            'file_type': 'file_type', 'iteration': 'iteration', 'upload_status': 'upload_status'
        })
        return f"File '{filename}' uploaded and processed.", df_ledger.to_dict('records')

    return f"Upload processed but ledger not found.", []

@app.callback(
    Output('download-link', 'children'),
    [Input('upload-table', 'selected_rows')],
    [State('upload-table', 'data'),
     State('planning-month-dropdown', 'value')]
)
def download_from_ledger(selected_rows, table_data, planning_month):
    if selected_rows and table_data:
        row = table_data[selected_rows[0]]
        if row['upload_status'].lower() == 'success':
            filename = f"output/enriched_{row['file_type']}_{planning_month.replace("'", '')}.xlsx"
            if os.path.exists(filename):
                return html.A("Download File", href=f"/download/{os.path.basename(filename)}", target="_blank")
    return ""

if __name__ == '__main__':
    app.run_server(debug=True)
