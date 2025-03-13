import pandas as pd

# Assuming email_dump and main_df are your dataframes
# email_dump has columns: received, subject, entity, cptyentity, amount, filepath
# main_df has columns: entity_code, entity_name, cpty, cpty_name, mat_date, category, comment

# Sample dataframes (replace with your actual data loading logic)
email_dump = pd.DataFrame({
    'received': ['2023-01-01', '2023-01-02'],
    'subject': ['Email 1', 'Email 2'],
    'entity': ['ENT1', 'ENT2'],
    'cptyentity': ['CPTY1', 'CPTY2'],
    'amount': [1000, 2000],
    'filepath': ['path/to/email1.msg', 'path/to/email2.msg']
})

main_df = pd.DataFrame({
    'entity_code': ['E1', 'E2'],
    'entity_name': ['ENT1', 'ENT3'],
    'cpty': ['C1', 'C2'],
    'cpty_name': ['CPTY1', 'CPTY3'],
    'mat_date': ['2023-01-01', '2023-01-02'],
    'category': ['CAT1', 'CAT2'],
    'comment': ['Comment1', 'Comment2']
})

# Function to append records to Excel with approval column
def append_to_excel(email_df, main_df, excel_file='IMCS.xlsx', sheet_name='Sheet2'):
    # Create a copy of main_df to avoid modifying the original
    output_df = main_df.copy()
    
    # Add Approval column initialized with empty string
    output_df['Approval'] = ''
    
    # Iterate through email_dump to find matches
    for index, email_row in email_df.iterrows():
        mask = (main_df['entity_name'] == email_row['entity']) & \
               (main_df['cpty_name'] == email_row['cptyentity'])
        matched_rows = main_df[mask]
        
        if not matched_rows.empty:
            # Append matched records to output_df with filepath in Approval column
            for _, matched_row in matched_rows.iterrows():
                new_row = matched_row.to_dict()
                new_row['Approval'] = email_row['filepath']
                output_df = pd.concat([output_df, pd.DataFrame([new_row])], ignore_index=True)
    
    # Save to Excel using openpyxl engine
    with pd.ExcelWriter(excel_file, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
        # If the sheet doesn't exist, it will be created; if it does, it will be overwritten
        output_df.to_excel(writer, sheet_name=sheet_name, index=False)

# Execute the function
append_to_excel(email_dump, main_df)

print("Data has been appended to IMCS.xlsx Sheet2 successfully!")