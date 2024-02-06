import pandas as pd

# Sample DataFrame
df = pd.DataFrame({
    'who_score': [1, 2, 3],
    'year': [2020, 2021, 2022],
    'total_who_cases': [50, 60, 70]
})

# Rename columns that contain 'who' to 'The WHO'
df.columns = ['The WHO' if 'who' in col else col for col in df.columns]

print(df)