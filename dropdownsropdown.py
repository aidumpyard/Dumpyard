import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
import calendar
import datetime

# Initialize the Dash app
app = dash.Dash(__name__)

# Generate the last 20 years for the Year dropdown
current_year = datetime.datetime.now().year
years_options = [{'label': str(year), 'value': year} for year in range(current_year-19, current_year+1)]

# Month names for the Month dropdown
month_names = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']

# Initial app layout
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
    html.Div(id='additional-dropdowns'),  # Placeholder for additional dropdowns
    html.Div(id='output-graphs')  # Placeholder for output graphs
])

# Callback to dynamically create additional dropdowns based on main-dropdown value
@app.callback(
    Output('additional-dropdowns', 'children'),
    Input('main-dropdown', 'value')
)
def update_dropdowns(selected_value):
    if selected_value == 'A2':
        return html.Div([
            dcc.Dropdown(
                id='month-dropdown',
                options=[{'label': month, 'value': month} for month in month_names],
                multi=True,
                placeholder="Select up to 4 months"
            ),
            dcc.Dropdown(
                id='year-dropdown',
                options=years_options,
                multi=True,
                placeholder="Select up to 4 years"
            )
        ])
    return html.Div()  # Return an empty div for A1 and A3 to prevent callback errors

# Callback to generate bar charts based on selected months and years
@app.callback(
    Output('output-graphs', 'children'),
    [Input('month-dropdown', 'value'),
     Input('year-dropdown', 'value')]
)
def update_output_graphs(selected_months, selected_years):
    # Prevent update if the dropdowns are not yet available or selections are empty
    if not selected_months or not selected_years:
        raise PreventUpdate

    graphs = []
    for year in selected_years:
        for month_name in selected_months:
            month = month_names.index(month_name) + 1  # Convert month name to number
            _, last_day = calendar.monthrange(year, month)
            days = [datetime.date(year, month, day) for day in range(1, last_day + 1)]
            saturdays = sum(1 for day in days if day.weekday() == 5)
            sundays = sum(1 for day in days if day.weekday() == 6)

            # Create a bar chart for the month and year
            data = [go.Bar(x=['Saturdays', 'Sundays'], y=[saturdays, sundays], name=f'{month_name} {year}')]
            layout = go.Layout(title=f'{month_name} {year}', xaxis=dict(title='Day'), yaxis=dict(title='Count'))
            fig = go.Figure(data=data, layout=layout)
            graphs.append(dcc.Graph(figure=fig))

    return graphs

if __name__ == '__main__':
    app.run_server(debug=True)