from datetime import datetime

def format_date(date_str, input_format="%Y-%m-%d"):
    # Parse the date string to a datetime object
    dt = datetime.strptime(date_str, input_format)
    
    # Define ordinal suffixes
    suffix = "th" if 11 <= dt.day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(dt.day % 10, "th")
    
    # Format the date
    formatted_date = dt.strftime(f"%-d{suffix} %b’%y")  # Use %-d for Linux/Mac, change to %#d for Windows
    return formatted_date

# Example usage
date_str = "2025-01-13"  # Input date string
formatted_date = format_date(date_str, "%Y-%m-%d")
print(formatted_date)