import pandas as pd
import numpy as np
from typing import Union, List, Dict

def load_data(file) -> Union[pd.DataFrame, str]:
    """Load data from uploaded file."""
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        else:
            return "Unsupported file format. Please upload CSV or Excel files."
        return df
    except Exception as e:
        return f"Error loading file: {str(e)}"

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate rows from dataframe."""
    return df.drop_duplicates()

def handle_missing_values(df: pd.DataFrame, strategy: Dict) -> pd.DataFrame:
    """Handle missing values based on user-defined strategy."""
    df_clean = df.copy()
    
    for column, method in strategy.items():
        if method == 'drop':
            df_clean = df_clean.dropna(subset=[column])
        elif method == 'mean':
            if pd.api.types.is_numeric_dtype(df_clean[column]):
                df_clean[column] = df_clean[column].fillna(df_clean[column].mean())
        elif method == 'median':
            if pd.api.types.is_numeric_dtype(df_clean[column]):
                df_clean[column] = df_clean[column].fillna(df_clean[column].median())
        elif method == 'mode':
            df_clean[column] = df_clean[column].fillna(df_clean[column].mode()[0])
        elif method == 'zero':
            df_clean[column] = df_clean[column].fillna(0)
            
    return df_clean

def fix_data_types(df: pd.DataFrame, type_mapping: Dict) -> pd.DataFrame:
    """Convert column data types based on mapping."""
    df_clean = df.copy()
    
    for column, dtype in type_mapping.items():
        try:
            if dtype == 'numeric':
                df_clean[column] = pd.to_numeric(df_clean[column], errors='coerce')
            elif dtype == 'datetime':
                df_clean[column] = pd.to_datetime(df_clean[column], errors='coerce')
            elif dtype == 'string':
                df_clean[column] = df_clean[column].astype(str)
        except Exception:
            continue
            
    return df_clean

def remove_outliers(df: pd.DataFrame, columns: List[str], method: str = 'iqr') -> pd.DataFrame:
    """Remove outliers from specified columns."""
    df_clean = df.copy()
    
    for column in columns:
        if not pd.api.types.is_numeric_dtype(df_clean[column]):
            continue
            
        if method == 'iqr':
            Q1 = df_clean[column].quantile(0.25)
            Q3 = df_clean[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df_clean = df_clean[(df_clean[column] >= lower_bound) & 
                              (df_clean[column] <= upper_bound)]
            
    return df_clean
