import streamlit as st
import pandas as pd
from utils.data_operations import (
    remove_duplicates, 
    handle_missing_values, 
    fix_data_types, 
    remove_outliers
)

def show_cleaning_options(df: pd.DataFrame):
    """Display and handle data cleaning options."""
    st.subheader("Data Cleaning Options")
    
    cleaned_df = df.copy()
    cleaning_performed = False
    
    # Duplicate removal
    if st.checkbox("Remove Duplicates"):
        cleaned_df = remove_duplicates(cleaned_df)
        cleaning_performed = True
        st.write(f"Removed {len(df) - len(cleaned_df)} duplicate rows")
    
    # Missing values handling
    if st.checkbox("Handle Missing Values"):
        st.write("Select strategy for handling missing values in each column:")
        missing_strategy = {}
        
        for column in cleaned_df.columns:
            missing_count = cleaned_df[column].isnull().sum()
            if missing_count > 0:
                st.write(f"{column}: {missing_count} missing values")
                strategy = st.selectbox(
                    f"Strategy for {column}",
                    ['drop', 'mean', 'median', 'mode', 'zero'],
                    key=f"missing_{column}"
                )
                missing_strategy[column] = strategy
        
        if missing_strategy:
            cleaned_df = handle_missing_values(cleaned_df, missing_strategy)
            cleaning_performed = True
    
    # Data type conversion
    if st.checkbox("Fix Data Types"):
        st.write("Select appropriate data type for each column:")
        type_mapping = {}
        
        for column in cleaned_df.columns:
            current_type = cleaned_df[column].dtype
            new_type = st.selectbox(
                f"Type for {column} (current: {current_type})",
                ['numeric', 'datetime', 'string'],
                key=f"type_{column}"
            )
            type_mapping[column] = new_type
        
        if type_mapping:
            cleaned_df = fix_data_types(cleaned_df, type_mapping)
            cleaning_performed = True
    
    # Outlier removal
    if st.checkbox("Remove Outliers"):
        numeric_columns = cleaned_df.select_dtypes(include=['int64', 'float64']).columns
        selected_columns = st.multiselect(
            "Select columns for outlier removal",
            numeric_columns
        )
        
        if selected_columns:
            method = st.selectbox(
                "Select outlier detection method",
                ['iqr']
            )
            cleaned_df = remove_outliers(cleaned_df, selected_columns, method)
            cleaning_performed = True
    
    return cleaned_df if cleaning_performed else None
