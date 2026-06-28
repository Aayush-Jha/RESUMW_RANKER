import os
import glob
import pandas as pd
from pathlib import Path


def discover_dataset_files(dataset_root):
    root = Path(dataset_root)
    if not root.exists():
        raise FileNotFoundError(f"Dataset root not found: {dataset_root}")

    files = []
    for path in root.rglob('*'):
        if path.is_file() and path.suffix.lower() in {'.txt', '.pdf', '.csv', '.docx'}:
            files.append(str(path))
    return sorted(files)


def build_demo_dataset(dataset_root):
    files = discover_dataset_files(dataset_root)
    rows = []
    for file_path in files:
        if file_path.lower().endswith('.csv'):
            continue
        rows.append({
            'source_path': file_path,
            'name': os.path.basename(file_path),
            'category': os.path.basename(os.path.dirname(file_path)),
        })
    return pd.DataFrame(rows)
