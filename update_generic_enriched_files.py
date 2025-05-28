import os
import pandas as pd

def update_monthly_generic_enriched(new_data, file_type, planning_month, config, base_dir='output'):
    month_key = planning_month.replace("'", "")
    enriched_file_path = os.path.join(base_dir, f"generic_enriched_{month_key}.xlsx")

    new_data['file_type'] = file_type

    if os.path.exists(enriched_file_path):
        existing_df = pd.read_excel(enriched_file_path)
        existing_df = existing_df[existing_df['file_type'] != file_type]
        combined_df = pd.concat([existing_df, new_data], ignore_index=True)
    else:
        combined_df = new_data.copy()

    sequence_df = config.FTP_Sequence[['file_type', 'Sequence']]
    combined_df = combined_df.merge(sequence_df, on='file_type', how='left')
    combined_df.sort_values(by=['Sequence'], inplace=True)
    combined_df.drop(columns=['Sequence'], inplace=True)

    combined_df.to_excel(enriched_file_path, index=False)
