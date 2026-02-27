"""
Data loading utilities for Enron email corpus.

Handles loading raw CSV dataset and resolving project paths.
"""

import pandas as pd
from pathlib import Path


def load_raw_data(data_filename: str = "enron_emails.csv") -> tuple[pd.DataFrame, Path]:
    """Load CSV, resolve project root, return (DataFrame, data_path)."""
    # Resolve project root
    project_root = Path.cwd()
    if not (project_root / "data").exists():
        project_root = Path.cwd().resolve().parents[1]
    
    data_path = project_root / "data" / "raw" / data_filename
    
    if not data_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {data_path}\n"
            f"Expected location: data/raw/{data_filename}"
        )
    
    df = pd.read_csv(data_path)
    
    return df, data_path
