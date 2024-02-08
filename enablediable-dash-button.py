# Import necessary libraries
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

# Create a Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = html.Div([
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Option 1', 'value': 'opt1'},
            {'label': 'Option 2', 'value': 'opt2'},
            {'label': 'Option 3', 'value': 'opt3'},  # Let's say we want to remove the button for this option
        ],
        value='opt1'  # Default value
    ),
    html.Br(),
    dbc.Button("Click Me", id="my-button", className="mr-2"),
])

# Callback to enable/disable or remove the button based on dropdown selection
@app.callback(
    Output("my-button", "disabled"),
    Output("my-button", "style"),
    Input("my-dropdown", "value"),
)
def update_button(selected_value):
    if selected_value == 'opt3':
        # Remove the button by hiding it when 'Option 3' is selected
        return True, {'display': 'none'}
    else:
        # Enable the button and make sure it's visible for other options
        return False, {'display': 'inline-block'}

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)