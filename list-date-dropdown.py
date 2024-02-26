import re
from datetime import datetime

# Sample list of strings
file_names = ['world_food_2014_02_01.csv', 'world_food_2015_03_15.csv', 'world_food_2016_12_25.csv']

# Function to convert the file name to the desired format
def convert_file_name(file_name):
    # Extract the date part using regular expressions
    date_part = re.search(r'(\d{4}_\d{2}_\d{2})', file_name)
    if date_part:
        # Convert the date part to the desired format
        date = datetime.strptime(date_part.group(), '%Y_%m_%d')
        return date.strftime('%d%B%Y')
    return None

# Convert the list of file names
converted_dates = [convert_file_name(file_name) for file_name in file_names]

# Print the converted dates
print(converted_dates)