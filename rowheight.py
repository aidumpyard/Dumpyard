import dash
from dash import dcc, html, dash_table
import pandas as pd

# Sample DataFrame
df = pd.DataFrame({
    'Column 1': ['A', 'B', 'C', 'D', 'E'],
    'Column 2': [1, 2, 3, 4, 5]
})

app = dash.Dash(__name__)

app.layout = html.Div([
    dash_table.DataTable(
        id='table',
        columns=[{'name': i, 'id': i} for i in df.columns],
        data=df.to_dict('records'),
        style_cell={
            'height': '30px',  # Reduce cell height to 30px
            'minWidth': '0px', 'maxWidth': '180px',
            'whiteSpace': 'normal'
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
    
