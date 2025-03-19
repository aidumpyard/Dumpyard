import pandas as pd

# Load email_dump dataframe (replace with actual loading method)
email_dump = pd.DataFrame({
    'received': ['2025-02-20 15:37:23', '2025-02-21 10:15:45'],
    'subject': ['Invoice A', 'Invoice B'],
    'entity': ['Entity1', 'Entity2'],
    'cptentity': ['CpEntity1', 'CpEntity2'],
    'amount': [1000, 2000],
    'filepath': ['path/to/file1', 'path/to/file2']
})

# Load ICT Mapping.xlsx
mapping_df = pd.read_excel("ICT Mapping.xlsx")  # Ensure this file is available

# Assuming ICT Mapping.xlsx has 'entity' and 'mapped_value' columns
entity_mapping = dict(zip(mapping_df['entity'], mapping_df['mapped_value']))
cptentity_mapping = dict(zip(mapping_df['cptentity'], mapping_df['mapped_value']))

# Map the values
email_dump['entity_mapped'] = email_dump['entity'].map(entity_mapping)
email_dump['cptentity_mapped'] = email_dump['cptentity'].map(cptentity_mapping)

# Convert received date to YYYY-MM-DD format
email_dump['received'] = pd.to_datetime(email_dump['received']).dt.date

# Display the result
import ace_tools as tools
tools.display_dataframe_to_user(name="Processed Email Dump", dataframe=email_dump)