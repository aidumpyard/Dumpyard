import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

# Sample data for demonstration
data = {
    'Category 1': pd.DataFrame({'X': [1, 2, 3], 'Y': [2, 3, 1], 'Label': ['A1', 'B1', 'C1']}),
    'Category 2': pd.DataFrame({'X': [4, 5, 6], 'Y': [7, 8, 6], 'Label': ['A2', 'B2', 'C2']}),
    'Category 3': pd.DataFrame({'X': [7, 8, 9], 'Y': [1, 2, 3], 'Label': ['A3', 'B3', 'C3']}),
    'Category 4': pd.DataFrame({'X': [10, 11, 12], 'Y': [9, 8, 7], 'Label': ['A4', 'B4', 'C4']})  # Assume no toggle needed
}

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='category-dropdown',
        options=[{'label': k, 'value': k} for k in data.keys()],
        placeholder="Select a category"
    ),
    html.Div(id='toggle-container'),
    dcc.Graph(id='scatter-chart'),
])

# Categories that require a toggle button
categories_with_toggle = ['Category 1', 'Category 2', 'Category 3']

@app.callback(
    Output('toggle-container', 'children'),
    [Input('category-dropdown', 'value')]
)
def update_toggle(selected_category):
    if selected_category in categories_with_toggle:
        return dcc.Checklist(
            id='toggle-button',
            options=[{'label': 'Show Data', 'value': 'SHOW'}],
            value=[]
        )
    return None  # Return None to not display the toggle button

@app.callback(
    Output('scatter-chart', 'figure'),
    [Input('category-dropdown', 'value'),
     Input('toggle-button', 'value')]
)
def update_chart(selected_category, toggle_value):
    if selected_category is None:
        return go.Figure()
    
    df = data[selected_category]
    show_labels = 'SHOW' in (toggle_value or [])
    
    trace = go.Scatter(
        x=df['X'],
        y=df['Y'],
        mode='markers+text' if show_labels else 'markers',
        text=df['Label'] if show_labels else None,
        textposition='top center'
    )
    
    return {
        'data': [trace],
        'layout': go.Layout(
            title=f'Scatter Chart for {selected_category}',
            xaxis={'title': 'X Axis'},
            yaxis={'title': 'Y Axis'}
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)