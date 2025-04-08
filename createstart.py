To write a DataFrame with a double header and grouping/ungrouping (expand/collapse) functionality for both columns and rows in Excel, you can use the openpyxl library. Here’s a complete working example:

import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.worksheet.dimensions import SheetFormatProperties

# Sample multi-index column data
columns = pd.MultiIndex.from_tuples([
    ('A', 'I'),
    ('A', 'J'),
    ('A', 'K'),
    ('B', 'L'),
    ('C', 'M'),
    ('C', 'N'),
    ('C', 'O')
])
data = [[f'{i}-{j}' for i, j in columns] for _ in range(8)]
df = pd.DataFrame(data, columns=columns)

# Create workbook and worksheet
wb = Workbook()
ws = wb.active
ws.title = "GroupedSheet"

# Write the headers and data manually to preserve multiindex structure
rows = dataframe_to_rows(df, index=False, header=True)
for r_idx, row in enumerate(rows, 1):
    ws.append(row)

# Group columns (A-C as one group, D as separate, E-G as another group)
# Columns are 1-based in openpyxl
# We group columns: 1-3 ("A"), 5-7 ("C")
ws.column_dimensions.group('A', 'C', hidden=False)
ws.column_dimensions.group('E', 'G', hidden=False)

# Group rows: say group rows 3-10 (data rows)
ws.row_dimensions.group(3, 10, hidden=False)

# Optionally, set outline properties to show +/- signs
ws.sheet_properties.outlinePr.summaryBelow = True  # Grouping icons below for rows
ws.sheet_properties.outlinePr.summaryRight = True  # Grouping icons to right for cols

# Save the workbook
wb.save("grouped_excel_output.xlsx")

Notes:
	•	This saves the file as grouped_excel_output.xlsx.
	•	Clicking the + / - buttons in Excel will expand/collapse the grouped columns and rows.
	•	Grouping by headers is done visually by column positions (1-based indexing: A=1, B=2, etc.).
	•	The DataFrame contains a MultiIndex for headers, replicating the double header concept.

Let me know if you’d like to color or freeze headers too.