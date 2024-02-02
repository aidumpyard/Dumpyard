import dash
from dash import dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Option 1', 'value': '1'},
            {'label': 'Option 2', 'value': '2'},
            {'label': 'Option 3', 'value': '3'},
        ],
        value='1'  # Default value
    ),
    html.Div(id='output-container-1'),
    html.Div(id='output-container-2'),
])

# Callback for the first output
@app.callback(
    Output('output-container-1', 'children'),
    [Input('my-dropdown', 'value')]
)
def update_output1(value):
    return f'You have selected "{value}" for the first output.'

# Callback for the second output
@app.callback(
    Output('output-container-2', 'children'),
    [Input('my-dropdown', 'value')]
)
def update_output2(value):
    return f'You have selected "{value}" for the second output, independently.'

if __name__ == '__main__':
    app.run_server(debug=True)