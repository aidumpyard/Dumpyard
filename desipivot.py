import pandas as pd

def create_pivot_table(input_data, filters, columns, rows, values, fields_to_rpt):
    # Apply filters to the input data
    for filter_col, filter_val in filters.items():
        input_data = input_data[input_data[filter_col].isin(filter_val)]
    
    # Create pivot table
    pivot_table = pd.pivot_table(
        input_data,
        index=rows,
        columns=columns,
        values=values,
        aggfunc=fields_to_rpt
    )
    
    return pivot_table

# Example usage
input_data = pd.read_excel('your_excel_file.xlsx')
filters = {'Region': ['North', 'South']}
columns = ['Product']
rows = ['Month']
values = ['Sales']
fields_to_rpt = {'Sales': 'sum'}

pivot_table = create_pivot_table(input_data, filters, columns, rows, values, fields_to_rpt)
print(pivot_table)