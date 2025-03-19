from datetime import datetime

# Input date string in ddmmyyyy format
date_str = "13012025"

# Convert string to datetime object
date_obj = datetime.strptime(date_str, "%d%m%Y")

# Format the date as "13 Jan’25"
formatted_date = date_obj.strftime("%d %b'%y")  # Corrected format

# Add ordinal suffix (st, nd, rd, th)
day = date_obj.day
if 10 <= day <= 20 or day % 10 not in {1, 2, 3}:
    suffix = "th"
else:
    suffix = {1: "st", 2: "nd", 3: "rd"}[day % 10]

# Final formatted date
final_date = f"{day}{suffix} {formatted_date[3:]}"
print(final_date)