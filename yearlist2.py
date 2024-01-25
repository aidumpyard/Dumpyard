import calendar

start_year = 2023  # Starting year
input_month = "Oct"  # Input month

# Find the month number for the input month
start_month_num = list(calendar.month_abbr).index(input_month)

months_years = []
current_year = start_year

for _ in range(6 * 12):  # 6 years * 12 months
    month_name = calendar.month_abbr[start_month_num]
    year_abbr = str(current_year)[-2:]
    formatted_date = f"{month_name}-{year_abbr}"
    months_years.append(formatted_date)

    # Increment month and year appropriately
    start_month_num += 1
    if start_month_num > 12:
        start_month_num = 1
        current_year += 1

print(months_years)