from dash import Dash, dcc, html, Input, Output, State
import plotly.graph_objs as go
import calendar
import datetime
from dash.exceptions import PreventUpdate

app = Dash(__name__)

current_year = datetime.datetime.now().year
years_options = [{'label': str(year), 'value': year} for year in range(current_year-19, current_year+1)]

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
    prevent_initial_call=True
)
def limit_selections(selected_months, selected_years):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'month-dropdown' and selected_months is not None:
        if len(selected_months) > 4:
            selected_months = selected_months[:4]

    if trigger_id == 'year-dropdown' and selected_years is not None:
        if len(selected_years) > 4:
            selected_years = selected_years[:4]

    return selected_months, selected_years

@app.callback(
    Output('output-graphs', 'children'),
    [Input('month-dropdown', 'value'),
     Input('year-dropdown', 'value')],
    prevent_initial_call=True
)
def update_output_graphs(selected_months, selected_years):
    if not selected_months or not selected_years:
        raise PreventUpdate

    graphs = []
    month_numbers = {month: i+1 for i, month in enumerate([
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'])}

    for year in selected_years:
        for month_name in selected_months:
            month = month_numbers[month_name]
            _, last_day = calendar.monthrange(year, month)
            days = [datetime.date(year, month, day) for day in range(1, last_day+1)]
            saturdays = sum(1 for day in days if day.weekday() == 5)
            sundays = sum(1 for day in days if day.weekday() == 6)

            data = [go.Bar(x=['Saturdays', 'Sundays'], y=[saturdays, sundays], name=f'{month_name} {year}')]
            layout = go.Layout(title=f'{month_name} {year}', xaxis=dict(title='Day'), yaxis=dict(title='Count'))
            fig = go.Figure(data=data, layout=layout)
            graphs.append(dcc.Graph(figure=fig))

    return graphs

if __name__ == '__main__':
    app.run_server(debug=True)