def xlookup(lookup_value, lookup_array, return_array, not_found=None):
    """
    Mimics Excel's XLOOKUP behavior.
    
    Args:
        lookup_value: The value to search for.
        lookup_array: The array (Series) to search in.
        return_array: The array (Series) to return value from.
        not_found: Value to return if not found.

    Returns:
        Corresponding value from return_array or not_found.
    """
    try:
        index = lookup_array[lookup_array == lookup_value].index
        if not index.empty:
            return return_array.loc[index[0]]
        return not_found
    except Exception as e:
        raise ValueError(f"XLOOKUP error: {e}")