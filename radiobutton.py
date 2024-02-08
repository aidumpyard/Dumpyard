import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

# Example DataFrame
df = pd.DataFrame({
    'X': [1, 2, 3, 4, 5],
    'Y': [2, 1, 4, 3, 5],
    'Value': ['A', 'B', 'C', 'D', 'E']  # Values to display on toggle
})

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='scatter-chart'),
    dcc.Checklist(
        id='toggle-button',
        options=[
            {'label': 'Show Values', 'value': 'SHOW'},
        ],
        value=[]
    )
])
@app.callback(
    Output('scatter-chart', 'figure'),
    [Input('toggle-button', 'value')]
)
def update_chart(toggle_value):
    trace = go.Scatter(
        x=df['X'],
        y=df['Y'],
        mode='markers+text' if 'SHOW' in toggle_value else 'markers',
        text=df['Value'] if 'SHOW' in toggle_value else None,  # Show or hide values
        textposition='top center'
    )
    
    return {
        'data': [trace],
        'layout': go.Layout(
            title='Scatter Chart',
            xaxis={'title': 'X Axis'},
            yaxis={'title': 'Y Axis'}
        )
    }
    
if __name__ == '__main__':
    app.run_server(debug=True)
