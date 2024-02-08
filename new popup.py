from dash import dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc  # Make sure to install dash-bootstrap-components

app.layout = html.Div([
    dcc.Dropdown(
        id='page-selection-dropdown',
        options=[
            {'label': 'Dataframe & Waterfall', 'value': 'page1'},
            {'label': 'Two Waterfalls', 'value': 'page2'},
            {'label': 'Scatter Charts', 'value': 'page3'}
        ],
        value='page1'  # Default value
    ),
    html.Div(id='page-content'),
    html.Button("Download", id="download-button"),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Select Pages to Download")),
        dbc.ModalBody([
            dcc.Dropdown(
                id='download-selection-dropdown',
                options=[
                    {'label': 'Dataframe & Waterfall', 'value': 'page1'},
                    {'label': 'Two Waterfalls', 'value': 'page2'},
                    {'label': 'Scatter Charts', 'value': 'page3'}
                ],
                value=['page1'],  # Default value
                multi=True
            )
        ]),
        dbc.ModalFooter(
            html.Button("Confirm Download", id="confirm-download", n_clicks=0)
        ),
    ], id="download-modal", is_open=False),
    dcc.Download(id="download-ppt")
])

@app.callback(
    Output("download-modal", "is_open"),
    [Input("download-button", "n_clicks"), Input("confirm-download", "n_clicks")],
    [State("download-modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("download-ppt", "data"),
    [Input("confirm-download", "n_clicks")],
    [State("download-selection-dropdown", "value")],
    prevent_initial_call=True,
)
def generate_ppt(n_clicks, selected_pages):
    if not n_clicks:
        raise PreventUpdate
    
    # Your existing logic to generate and download the PPT based on selected_pages
