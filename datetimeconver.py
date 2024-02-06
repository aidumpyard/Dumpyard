from datetime import datetime

# Example filename
filename = "20230207_example_file.txt"

# Step 1: Extract the date part from the filename
date_str = filename.split("_")[0]

# Step 2: Parse the date string into a datetime object
date_obj = datetime.strptime(date_str, "%Y%m%d")

# Step 3: Format the datetime object into DD-MON-YY format
formatted_date = date_obj.strftime("%d-%b-%y")

print(formatted_date)