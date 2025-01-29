import pandas as pd

# Load Excel file
file_path = "your_file.xlsx"
xl = pd.ExcelFile(file_path)

# Define mapping dictionary for 'Cpty Entity'
cpty_mapping = {
    "OldValue1": "MappedValue1",
    "OldValue2": "MappedValue2",
    # Add more mappings as needed
}

# Read all sheets into a dictionary
sheets_data = {sheet: xl.parse(sheet) for sheet in xl.sheet_names}

# Process the ND sheet
if 'ND' in sheets_data:
    df = sheets_data['ND']

    # Apply filter on column 'x'
    df = df[df['x'] == "New Deal - New"]

    # Keep only rows where tenure is greater than 7
    df = df[df['tenure'] > 7]

    # Remove records where 'Entity' and 'Cpty Entity' are not empty
    df = df[(df['Entity'].isna()) & (df['Cpty Entity'].isna())]

    # Map 'Cpty Entity' using dictionary
    df['Mapped Cpty Entity'] = df['Cpty Entity'].map(cpty_mapping).fillna(df['Cpty Entity'])

    # Remove rows where 'Mapped Cpty Entity' is the same as 'Cpty Entity'
    df = df[df['Mapped Cpty Entity'] != df['Cpty Entity']]

    # Save back to the dictionary
    sheets_data['ND'] = df

# Save the modified data to a new Excel file
output_file = "filtered_output.xlsx"
with pd.ExcelWriter(output_file) as writer:
    for sheet, data in sheets_data.items():
        data.to_excel(writer, sheet_name=sheet, index=False)

print("Processing completed. Filtered file saved as:", output_file)