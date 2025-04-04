import pandas as pd

def vlookup(lookup_value, lookup_df, lookup_column, return_column, exact_match=True):
    """
    Mimics Excel's VLOOKUP for pandas DataFrames.
    
    Args:
        lookup_value: Value to look up.
        lookup_df: pandas DataFrame to search.
        lookup_column: Column name to search in.
        return_column: Column name from which to return the value.
        exact_match: Whether to match exactly (default True).

    Returns:
        Matched value or None if not found.
    """
    try:
        if exact_match:
            match = lookup_df[lookup_df[lookup_column] == lookup_value]
        else:
            match = lookup_df[lookup_df[lookup_column] <= lookup_value].sort_values(by=lookup_column, ascending=False)

        if not match.empty:
            return match.iloc[0][return_column]
        else:
            return None
    except Exception as e:
        raise ValueError(f"VLOOKUP error: {e}")