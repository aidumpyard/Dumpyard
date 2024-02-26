import dash
from dash import html
from dash import dcc
from dash import dash_table
import pandas as pd

# Sample DataFrame with mixed data types
df = pd.DataFrame({
    "Column 1": [1, -2, 3, -4, 5],
    "Column 2": [10, -20, 30, -40, 50],
    "Column 3": ["A", "B", "C", "D", "E"]
})

# Function to format negative numbers
def format_negative_numbers(value):
    return f"({abs(value)})" if isinstance(value, (int, float)) and value < 0 else value

# Apply the formatting function to the DataFrame
formatted_df = df.applymap(format_negative_numbers)

app = dash.Dash(__name__)

app.layout = html.Div([
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=formatted_df.to_dict('records'),
        style_data_conditional=[
            {
                'if': {'filter_query': '{{{}}} < 0'.format(col)},
                'color': 'red'  # Optional: change the text color for negative numbers
            } for col in df.columns if df[col].dtype in [int, float]
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)