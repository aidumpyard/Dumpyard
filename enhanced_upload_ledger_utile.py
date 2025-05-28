import pandas as pd
import os

def load_upload_ledger_from_config(config, planning_month, ledger_file='uploader_ledger.xlsx'):
    df_config = config.FTP_Sequence[['file_type', 'flow_type', 'Sequence']].copy()
    df_config.sort_values(by='Sequence', inplace=True)

    if os.path.exists(ledger_file):
        xl = pd.ExcelFile(ledger_file)
        if planning_month in xl.sheet_names:
            df_ledger = xl.parse(planning_month)
            df_merged = df_config.merge(df_ledger, on='file_type', how='left')
            df_merged['upload_status'] = df_merged['upload_status'].fillna('Yet to Upload')
            df_merged['iteration'] = df_merged['iteration'].fillna(0).astype(int)
        else:
            df_merged = df_config.copy()
            df_merged['upload_status'] = 'Yet to Upload'
            df_merged['iteration'] = 0
    else:
        df_merged = df_config.copy()
        df_merged['upload_status'] = 'Yet to Upload'
        df_merged['iteration'] = 0

    return df_merged[['file_type', 'iteration', 'upload_status']]
