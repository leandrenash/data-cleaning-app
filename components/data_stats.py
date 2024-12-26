import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_validation import get_missing_values_info, get_duplicate_info

def show_data_statistics(df: pd.DataFrame):
    """Display detailed statistics about the dataset."""
    st.subheader("Data Statistics")
    
    # Missing values visualization
    missing_values = get_missing_values_info(df)
    if any(missing_values.values()):
        st.write("Missing Values Distribution:")
        fig = px.bar(
            x=list(missing_values.keys()),
            y=list(missing_values.values()),
            labels={'x': 'Column', 'y': 'Missing Values (%)'},
            title='Missing Values by Column'
        )
        st.plotly_chart(fig)
    
    # Duplicate rows information
    num_duplicates, _ = get_duplicate_info(df)
    if num_duplicates > 0:
        st.write(f"Number of duplicate rows: {num_duplicates}")
    
    # Numerical columns distribution
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    if len(numeric_cols) > 0:
        selected_col = st.selectbox(
            "Select column for distribution plot",
            numeric_cols
        )
        
        fig = px.histogram(
            df,
            x=selected_col,
            title=f'Distribution of {selected_col}'
        )
        st.plotly_chart(fig)
        
        # Box plot for outlier visualization
        fig = px.box(
            df,
            y=selected_col,
            title=f'Box Plot of {selected_col}'
        )
        st.plotly_chart(fig)
