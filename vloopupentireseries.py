def vlookup_series(series, lookup_df, lookup_column, return_column, exact_match=True):
    return series.apply(lambda x: vlookup(x, lookup_df, lookup_column, return_column, exact_match))