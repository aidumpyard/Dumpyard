import pandas as pd
from lookup_utils.vlookup import vlookup, vlookup_series
from lookup_utils.xlookup import xlookup
from lookup_utils.exceptions import VLookupError, XLookupError

def run_lookups():
    # Sample data
    data_main = pd.DataFrame({
        'ID': [1, 2, 3, 4],
        'Name': ['Alice', 'Bob', 'Charlie', 'David']
    })

    lookup_table = pd.DataFrame({
        'ID': [1, 2, 3],
        'Department': ['HR', 'Finance', 'Engineering']
    })

    try:
        # Single value VLOOKUP
        dept = vlookup(2, lookup_table, 'ID', 'Department')
        print(f"Department for ID 2: {dept}")

        # Series-based VLOOKUP
        data_main['Department'] = vlookup_series(data_main['ID'], lookup_table, 'ID', 'Department')
        print("\nData after vlookup:\n", data_main)

        # XLOOKUP Example
        department_series = lookup_table['Department']
        id_series = lookup_table['ID']
        result = xlookup(3, id_series, department_series, not_found="Not Found")
        print(f"\nXLOOKUP result for ID 3: {result}")

    except VLookupError as ve:
        print(f"VLookup Error: {ve}")
    except XLookupError as xe:
        print(f"XLookup Error: {xe}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    run_lookups()