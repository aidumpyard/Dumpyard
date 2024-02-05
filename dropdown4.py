from dash import Dash, dcc, html, Input, Output, State, ctx
import plotly.graph_objs as go
import calendar
import datetime

app = Dash(__name__)

current_year = datetime.datetime.now().year
years = list(range(current_year-19, current_year+1))
years_options = [{'label': str(year), 'value': year} for year in years]

app.layout = html.Div([
    dcc.Dropdown(
        id='main-dropdown',
        options=[
            {'label': 'A1', 'value': 'A1'},
            {'label': 'A2', 'value': 'A2'},
            {'label': 'A3', 'value': 'A3'}
        ],
        value='A1'  # Default value
    ),
    html.Div(id='dynamic-dropdown-container', style={'display': 'none'}, children=[
        dcc.Dropdown(
            id='month-dropdown',
            options=[{'label': month, 'value': month} for month in [
                'January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'
            ]],
            multi=True,
            placeholder="Select up to 4 months",
        ),
        dcc.Dropdown(
            id='year-dropdown',
            options=years_options,
            multi=True,
            placeholder="Select up to 4 years",
        )
    ]),
    html.Div(id='output-graphs')  # Placeholder for graphs
])

@app.callback(
    Output('dynamic-dropdown-container', 'style'),
    Input('main-dropdown', 'value')
)
def show_hide_element(visibility_state):
    if visibility_state == 'A2':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(
    [Output('month-dropdown', 'value'),
     Output('year-dropdown', 'value')],
    [Input('month-dropdown', 'value'),
     Input('year-dropdown', 'value')],
    [State('month-dropdown', 'value'),
     State('year-dropdown', 'value')]
)
def limit_selections(selected_months, selected_years, prev_selected_months, prev_selected_years):
    # Triggering ID to identify which dropdown triggered the callback
    trigger_id = ctx.triggered_id

    if trigger_id == 'month-dropdown' and selected_months is not None:
        if len(selected_months) > 4:
            selected_months = selected_months[:4]

    if trigger_id == 'year-dropdown' and selected_years is not None:
        if len(selected_years) > 4:
            selected_years = selected_years[:4]

    return selected_months, selected_years

# Add your existing callback for generating graphs here

if __name__ == '__main__':
    app.run_server(debug=True)