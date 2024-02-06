import re
from datetime import datetime

# Sample file names with dates in various positions and cases
file_names = [
    "20230101_examplefile.txt",
    "example_25Dec22_file.doc",
    "anotherfile_20211225.pdf",
    "file_01jan23_middle.txt"
]

# Regular expressions for different date formats with re.IGNORECASE for DDMONYY
date_patterns = {
    'YYYYMMDD': re.compile(r'(\d{4})(\d{2})(\d{2})'),  # Matches YYYYMMDD
    'DDMONYY': re.compile(r'(\d{2})([a-zA-Z]{3})(\d{2})', re.IGNORECASE),  # Matches DDMONYY in any case
}

# Function to parse date from file name
def parse_date_from_filename(filename):
    for format, pattern in date_patterns.items():
        match = pattern.search(filename)
        if match:
            if format == 'YYYYMMDD':
                date = datetime.strptime(f"{match.group(1)}{match.group(2)}{match.group(3)}", '%Y%m%d')
            elif format == 'DDMONYY':
                month = match.group(2).capitalize()  # Ensure the month is in the correct case
                date_str = f"{match.group(1)}{month}{match.group(3)}"
                date = datetime.strptime(date_str, '%d%b%y')
            else:
                return None  # No recognized date format found
            
            # Format the date as "DD-MON-YY"
            return date.strftime('%d-%b-%y').upper()  # Convert to uppercase to match the desired output

# Try parsing each file name and print the formatted date
for file_name in file_names:
    formatted_date = parse_date_from_filename(file_name)
    print(f"File: {file_name}, Date: {formatted_date}")