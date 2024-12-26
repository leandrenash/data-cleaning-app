import pandas as pd
from typing import Dict, List, Tuple

def get_column_types(df: pd.DataFrame) -> Dict[str, str]:
    """Get data types of all columns."""
    type_map = {}
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            type_map[column] = 'numeric'
        elif pd.api.types.is_datetime64_dtype(df[column]):
            type_map[column] = 'datetime'
        else:
            type_map[column] = 'string'
    return type_map

def get_missing_values_info(df: pd.DataFrame) -> Dict[str, float]:
    """Get percentage of missing values for each column."""
    return (df.isnull().sum() / len(df) * 100).to_dict()

def get_duplicate_info(df: pd.DataFrame) -> Tuple[int, List[str]]:
    """Get information about duplicate rows."""
    duplicates = df.duplicated()
    num_duplicates = duplicates.sum()
    duplicate_indices = df[duplicates].index.tolist()
    return num_duplicates, duplicate_indices

def validate_data_types(df: pd.DataFrame) -> Dict[str, List[str]]:
    """Validate data types and return potential issues."""
    issues = {}
    for column in df.columns:
        column_issues = []
        if pd.api.types.is_numeric_dtype(df[column]):
            non_numeric = df[pd.to_numeric(df[column], errors='coerce').isna()][column]
            if len(non_numeric) > 0:
                column_issues.append(f"Contains {len(non_numeric)} non-numeric values")
        if len(column_issues) > 0:
            issues[column] = column_issues
    return issues
