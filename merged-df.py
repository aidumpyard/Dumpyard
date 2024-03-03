import pandas as pd

# Sample data for DF1 and DF2
data1 = {
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9],
    'D': [10, 11, 12]
}

data2 = {
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [10, 11, 12],
    'D': [13, 14, 15]
}

DF1 = pd.DataFrame(data1)
DF2 = pd.DataFrame(data2)

# Create DF_delta with the differences in columns C and D
DF_delta = DF2.copy()
DF_delta['C'] = DF2['C'] - DF1['C']
DF_delta['D'] = DF2['D'] - DF1['D']

# Merge DF1, DF2, and DF_delta on columns A and B
merged_df = pd.merge(DF1, DF2, on=['A', 'B'], suffixes=('_DF1', '_DF2'))
merged_df = pd.merge(merged_df, DF_delta, on=['A', 'B'], suffixes=('', '_delta'))

print("DF1:")
print(DF1)
print("\nDF2:")
print(DF2)
print("\nDF_delta:")
print(DF_delta)
print("\nMerged DataFrame:")
print(merged_df)