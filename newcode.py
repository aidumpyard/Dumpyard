import os
import zipfile

# Directory structure
base_dir = "/mnt/data/data_pipeline_project"
dirs = [
    "input_handler",
    "processing",
    "orchestrator",
    "utils",
    "output"
]

files = {
    "main.py": """
from orchestrator.pipeline_manager import PipelineManager

if __name__ == "__main__":
    # Replace this list with actual xlsx file paths
    input_files = ["data/file1.xlsx", "data/file2.xlsx"]
    pipeline = PipelineManager()
    pipeline.run_pipeline(input_files)
""",

    "config.py": """
# Configuration settings
CHECKPOINT_FILE = 'checkpoints.json'
OUTPUT_FILE = 'output/final_output.csv'
""",

    "input_handler/loader_factory.py": """
from input_handler.xlsx_loader import XLSXLoader

class LoaderFactory:
    @staticmethod
    def get_loader(file_path: str):
        return XLSXLoader(file_path)
""",

    "input_handler/xlsx_loader.py": """
import pandas as pd

class XLSXLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        return pd.read_excel(self.file_path)
""",

    "processing/cleaner.py": """
class DataCleaner:
    def clean(self, df):
        return df.dropna()
""",

    "processing/formatter.py": """
class DataFormatter:
    def format(self, df):
        # Standard formatting logic
        return df
""",

    "processing/schema_unifier.py": """
class SchemaUnifier:
    def unify(self, df):
        # Map columns to a standard schema
        df.columns = [col.lower().strip() for col in df.columns]
        return df
""",

    "orchestrator/pipeline_manager.py": """
import os
from concurrent.futures import ThreadPoolExecutor
from input_handler.loader_factory import LoaderFactory
from processing.cleaner import DataCleaner
from processing.formatter import DataFormatter
from processing.schema_unifier import SchemaUnifier
from orchestrator.checkpoint_manager import CheckpointManager

class PipelineManager:
    def __init__(self):
        self.checkpoint = CheckpointManager()
        self.processed_files = self.checkpoint.load()
        self.cleaner = DataCleaner()
        self.formatter = DataFormatter()
        self.unifier = SchemaUnifier()

    def run_pipeline(self, file_list):
        to_process = [f for f in file_list if f not in self.processed_files]
        with ThreadPoolExecutor() as executor:
            executor.map(self.handle_file, to_process)
        self.checkpoint.save(to_process + self.processed_files)

    def handle_file(self, file_path):
        loader = LoaderFactory.get_loader(file_path)
        df = loader.load()
        df_clean = self.cleaner.clean(df)
        df_format = self.formatter.format(df_clean)
        df_unified = self.unifier.unify(df_format)
        df_unified.to_parquet(f"output/{os.path.basename(file_path)}.parquet", index=False)
""",

    "orchestrator/checkpoint_manager.py": """
import json
import os
from config import CHECKPOINT_FILE

class CheckpointManager:
    def __init__(self, path=CHECKPOINT_FILE):
        self.path = path

    def save(self, processed_files):
        with open(self.path, 'w') as f:
            json.dump(processed_files, f)

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                return json.load(f)
        return []
""",

    "utils/logger.py": """
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
""",

    "output/output_writer.py": """
import pandas as pd

def generate_final_output(current_files, last_month_data_path):
    dfs = [pd.read_parquet(f) for f in current_files]
    df_combined = pd.concat(dfs)
    df_last = pd.read_parquet(last_month_data_path)
    final_df = pd.concat([df_last, df_combined])
    final_df.to_csv("output/final_output.csv", index=False)
"""
}

# Create directories
for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

# Write files
for path, content in files.items():
    with open(os.path.join(base_dir, path), 'w') as f:
        f.write(content.strip())

# Zip the folder
zip_path = "/mnt/data/data_pipeline_project.zip"
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, _, filenames in os.walk(base_dir):
        for file in filenames:
            file_path = os.path.join(root, file)
            zipf.write(file_path, os.path.relpath(file_path, base_dir))

zip_path