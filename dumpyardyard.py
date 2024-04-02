import dash
from dash import dcc, html
import dash_table
import pandas as pd

# Sample data
data = [
    {'name': 'Alice', 'age': 24, 'city': 'New York', 'country': 'USA', 'occupation': 'Engineer'},
    {'name': 'blank', 'age': 30, 'city': 'London', 'country': 'UK', 'occupation': 'Doctor'},
    {'name': 'Charlie', 'age': 35, 'city': 'Paris', 'country': 'France', 'occupation': 'Artist'},
    {'name': 'blank', 'age': 28, 'city': 'Berlin', 'country': 'Germany', 'occupation': 'Teacher'}
]

df = pd.DataFrame(data)

# Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{name} = "blank"',
                },
                'height': '20px',  # Half the height of other rows
            }
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)