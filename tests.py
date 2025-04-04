from lookup_utils.vlookup import vlookup
import pandas as pd

def test_vlookup_exact():
    df = pd.DataFrame({'Key': [1, 2, 3], 'Value': ['A', 'B', 'C']})
    assert vlookup(2, df, 'Key', 'Value') == 'B'