import streamlit as st
import pandas as pd

def show_data_preview(df: pd.DataFrame):
    """Display data preview with basic information."""
    st.subheader("Data Preview")
    
    # Show basic information
    st.write("Dataset Shape:", df.shape)
    st.write("Number of Columns:", len(df.columns))
    st.write("Number of Rows:", len(df))
    
    # Column information
    st.write("Columns:", ", ".join(df.columns))
    
    # Preview first few rows
    st.write("First few rows of the dataset:")
    st.dataframe(df.head())
    
    # Data types
    st.write("Data Types:")
    st.dataframe(pd.DataFrame({'Data Type': df.dtypes}))

def show_column_statistics(df: pd.DataFrame):
    """Display basic statistics for numerical columns."""
    st.subheader("Column Statistics")
    
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    if len(numeric_cols) > 0:
        st.write("Numerical Columns Statistics:")
        st.dataframe(df[numeric_cols].describe())
    
    categorical_cols = df.select_dtypes(include=['object']).columns
    if len(categorical_cols) > 0:
        st.write("Categorical Columns Value Counts:")
        for col in categorical_cols:
            st.write(f"\nUnique values in {col}:")
            st.write(df[col].value_counts().head())
