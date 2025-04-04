import pandas as pd
from .xlookup import xlookup

def xlookup_series(lookup_series, lookup_array, return_array, not_found=None):
    """
    Apply XLOOKUP on a pandas Series.

    Args:
        lookup_series (pd.Series): Series of values to look up.
        lookup_array (pd.Series): Series to search in.
        return_array (pd.Series): Series to return values from.
        not_found: Default value if lookup value is not found.

    Returns:
        pd.Series with matched values.
    """
    return lookup_series.apply(lambda val: xlookup(val, lookup_array, return_array, not_found))