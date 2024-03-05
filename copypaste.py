# Insert a blank row between rows 2 and 3
worksheet.insert_rows(3)

# Copy data from the first 4 columns and 3 rows to the 12th row starting from the 7th column
for row in range(1, 4):
    for col in range(1, 5):
        src_cell = worksheet.cell(row=row, column=col)
        dest_cell = worksheet.cell(row=row + 11, column=col + 6)  # Adjust the destination row and column
        dest_cell.value = src_cell.value

        # Copy the style if needed
        if src_cell.has_style:
            dest_cell.font = copy(src_cell.font)
            dest_cell.border = copy(src_cell.border)
            dest_cell.fill = copy(src_cell.fill)
            dest_cell.number_format = copy(src_cell.number_format)
            dest_cell.protection = copy(src_cell.protection)
            dest_cell.alignment = copy(src_cell.alignment)