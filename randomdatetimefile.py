import re
from datetime import datetime

# Sample file names with dates in various positions
file_names = [
    "20230101_examplefile.txt", 
    "example_25DEC22_file.doc",
    "anotherfile_20211225.pdf",
    "file_01JAN23_middle.txt"
]

# Regular expressions for different date formats
# These patterns now are more generic and can match dates anywhere in the string
date_patterns = {
    'YYYYMMDD': re.compile(r'(\d{4})(\d{2})(\d{2})'),  # Matches YYYYMMDD
    'DDMONYY': re.compile(r'(\d{2})([A-Z]{3})(\d{2})'),  # Matches DDMONYY
}

# Function to parse date from file name
def parse_date_from_filename(filename):
    for format, pattern in date_patterns.items():
        match = pattern.search(filename)
        if match:
            if format == 'YYYYMMDD':
                # Directly use matched groups to form a date string and parse it
                return datetime.strptime(f"{match.group(1)}{match.group(2)}{match.group(3)}", '%Y%m%d')
            elif format == 'DDMONYY':
                # For DDMONYY, the month is in text format, so we use it directly
                return datetime.strptime(f"{match.group(1)}{match.group(2)}{match.group(3)}", '%d%b%y')
    return None  # No recognized date format found

# Try parsing each file name
for file_name in file_names:
    date = parse_date_from_filename(file_name)
    print(f"File: {file_name}, Date: {date}")