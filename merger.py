import dash
import dash_table
import pandas as pd
from dash import html

# Sample data
data_summary1 = {
    'Currency': ['USD', 'EUR', 'GBP', 'JPY'],
    'Column1': [1, 2, 3, 4],
    'Column2': [5, 6, 7, 8],
    'Column3': [9, 10, 11, 12],
    'Column4': [13, 14, 15, 16],
    'Column5': [17, 18, 19, 20],
    'Column6': [21, 22, 23, 24]
}

data_summary2 = {
    'Currency': ['USD', 'EUR', 'GBP', 'JPY'],
    'Column1': [25, 26, 27, 28],
    'Column2': [29, 30, 31, 32],
    'Column3': [33, 34, 35, 36],
    'Column4': [37, 38, 39, 40],
    'Column5': [41, 42, 43, 44],
    'Column6': [45, 46, 47, 48]
}

df_summary1 = pd.DataFrame(data_summary1)
df_summary2 = pd.DataFrame(data_summary2)

# Merge the dataframes on the 'Currency' column
merged_df = pd.merge(df_summary1, df_summary2, on='Currency', suffixes=('_Summary1', '_Summary2'))

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dash_table.DataTable(
        id='merged-table',
        columns=[
            {"name": ['', 'Currency'], "id": 'Currency'},
            {"name": ['DF Summary1', 'Column1'], "id": 'Column1_Summary1'},
            {"name": ['DF Summary1', 'Column2'], "id": 'Column2_Summary1'},
            {"name": ['DF Summary1', 'Column3'], "id": 'Column3_Summary1'},
            {"name": ['DF Summary1', 'Column4'], "id": 'Column4_Summary1'},
            {"name": ['DF Summary1', 'Column5'], "id": 'Column5_Summary1'},
            {"name": ['DF Summary1', 'Column6'], "id": 'Column6_Summary1'},
            {"name": ['DF Summary2', 'Column1'], "id": 'Column1_Summary2'},
            {"name": ['DF Summary2', 'Column2'], "id": 'Column2_Summary2'},
            {"name": ['DF Summary2', 'Column3'], "id": 'Column3_Summary2'},
            {"name": ['DF Summary2', 'Column4'], "id": 'Column4_Summary2'},
            {"name": ['DF Summary2', 'Column5'], "id": 'Column5_Summary2'},
            {"name": ['DF Summary2', 'Column6'], "id": 'Column6_Summary2'}
        ],
        data=merged_df.to_dict('records'),
        merge_duplicate_headers=True
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)