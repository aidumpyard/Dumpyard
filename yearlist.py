import calendar

start_year = 2023
end_year = start_year + 6  # 6 consecutive years including the start year
months_years = []

for year in range(start_year, end_year):
    for month in range(1, 13):
        month_name = calendar.month_abbr[month]
        year_abbr = str(year)[-2:]
        formatted_date = f"{month_name}-{year_abbr}"
        months_years.append(formatted_date)

print(months_years)