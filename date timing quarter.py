def convert_to_month_year_quarter(date_str):
    # Parsing the date
    parsed_date = datetime.strptime(date_str, '%d-%b-%y')
    month = parsed_date.strftime('%b')
    year = parsed_date.strftime('%Y')

    # Determining the quarter
    month_num = parsed_date.month
    quarter = (month_num - 1) // 3 + 1

    return month, year, f"Q{quarter}"

# Example
convert_to_month_year_quarter("18-OCT-23")