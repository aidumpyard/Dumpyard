# utils.py

import pandas as pd

def validate_lookup_args(lookup_df, lookup_column, return_column):
    if not isinstance(lookup_df, pd.DataFrame):
        raise TypeError("lookup_df must be a pandas DataFrame.")
    
    if lookup_column not in lookup_df.columns:
        raise ValueError(f"lookup_column '{lookup_column}' not found in DataFrame.")

    if return_column not in lookup_df.columns:
        raise ValueError(f"return_column '{return_column}' not found in DataFrame.")
        
        
        
from .utils import validate_lookup_args
from .exceptions import VLookupError



try:
    validate_lookup_args(lookup_df, lookup_column, return_column)
    ...
except Exception as e:
    raise VLookupError(str(e))


        
        