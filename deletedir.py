import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path

def delete_directories_older_than_days(root_path: str, days: int):
    root = Path(root_path)
    now = datetime.now()
    threshold = now - timedelta(days=days)
    
    for item in root.rglob('*'):  # Recursively goes through all files and directories
        if item.is_dir():  # Check if it is a directory
            try:
                mtime = datetime.fromtimestamp(item.stat().st_mtime)
                if mtime < threshold:
                    shutil.rmtree(item)
                    print(f"Deleted {item} as it was last modified on {mtime}")
            except Exception as e:
                print(f"Error deleting {item}: {e}")

# Example usage
if __name__ == "__main__":
    directory_to_clean = "/path/to/your/directory"
    days_old = 5
    delete_directories_older_than_days(directory_to_clean, days_old)