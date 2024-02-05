import calendar
import plotly.graph_objs as go
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash
import datetime

# Initialize the Dash app
app = dash.Dash(__name__)

# Generate the last 20 years for the Year dropdown
current_year = datetime.datetime.now().year
years_options = [{'label': str(year), 'value': year} for year in range(current_year-19, current_year+1)]

# App layout
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

# Callback to dynamically create additional dropdowns
@app.callback(
    Output('additional-dropdowns', 'children'),
    Input('main-dropdown', 'value')
)
def update_dropdowns(selected_value):
    if selected_value == 'A2':
        return html.Div([
            dcc.Dropdown(
                id='month-dropdown',
                options=[{'label': month, 'value': month} for month in [
                    'January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December'
                ]],
                multi=True,
                placeholder="Select up to 4 months",
                value=[]  # Default value
            ),
            dcc.Dropdown(
                id='year-dropdown',
                options=years_options,
                multi=True,
                placeholder="Select up to 4 years",
                value=[]  # Default value
            )
        ])
    else:
        return html.Div()  # Return an empty div if A2 is not selected

# Callback to generate bar charts based on month and year selection
@app.callback(
    Output('output-graphs', 'children'),
    [Input('month-dropdown', 'value'),
     Input('year-dropdown', 'value')]
)
def update_output_graphs(selected_months, selected_years):
    graphs = []
    month_numbers = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                     'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
    
    for year in selected_years:
        for month_name in selected_months:
            month = month_numbers[month_name]
            _, last_day = calendar.monthrange(year, month)
            days = [datetime.date(year, month, day) for day in range(1, last_day+1)]
            saturdays = sum(1 for day in days if day.weekday() == 5)
            sundays = sum(1 for day in days if day.weekday() == 6)
            
            # Create bar chart for the month and year
            data = [go.Bar(x=['Saturdays', 'Sundays'], y=[saturdays, sundays], name=f'{month_name} {year}')]
            layout = go.Layout(title=f'{month_name} {year}', xaxis=dict(title='Day'), yaxis=dict(title='Count'))
            fig = go.Figure(data=data, layout=layout)
            graph = dcc.Graph(figure=fig)
            graphs.append(graph)
            
    return graphs

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)