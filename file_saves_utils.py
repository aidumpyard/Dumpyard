import os
import shutil
import pandas as pd
from datetime import datetime

def get_year_and_month(planning_month):
    month_map = {
        'Jan': 'January', 'Feb': 'February', 'Mar': 'March', 'Apr': 'April',
        'May': 'May', 'Jun': 'June', 'Jul': 'July', 'Aug': 'August',
        'Sep': 'September', 'Oct': 'October', 'Nov': 'November', 'Dec': 'December'
    }
    short_month = planning_month[:3]
    year_suffix = planning_month[-2:]
    full_year = f"20{year_suffix}"
    full_month = month_map.get(short_month, short_month)
    return full_year, full_month

def save_with_iteration(df, file_type, iteration, planning_month, status="Success", base_dir="output"):
    year, month = get_year_and_month(planning_month)
    month_dir = os.path.join(base_dir, year, month)
    archive_dir = os.path.join(month_dir, "archive")
    archive_log = os.path.join(month_dir, "archive_log.csv")

    os.makedirs(month_dir, exist_ok=True)
    os.makedirs(archive_dir, exist_ok=True)

    new_filename = f"{file_type}_v{iteration}.xlsx"
    file_path = os.path.join(month_dir, new_filename)

    for existing_file in os.listdir(month_dir):
        if existing_file.startswith(file_type) and existing_file.endswith('.xlsx') and existing_file != new_filename:
            src_path = os.path.join(month_dir, existing_file)
            dst_path = os.path.join(archive_dir, existing_file)
            shutil.move(src_path, dst_path)
            log_archived_file(archive_log, src_path, dst_path, file_type, iteration, "Archived")

    df.to_excel(file_path, index=False)
    return file_path

def log_archived_file(log_path, original_path, archive_path, file_type, iteration, status):
    log_entry = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "File Type": file_type,
        "Iteration": iteration,
        "Status": status,
        "Original File Path": original_path,
        "Archived File Path": archive_path
    }
    if os.path.exists(log_path):
        log_df = pd.read_csv(log_path)
        log_df = pd.concat([log_df, pd.DataFrame([log_entry])], ignore_index=True)
    else:
        log_df = pd.DataFrame([log_entry])
    log_df.to_csv(log_path, index=False)
