import streamlit as st
import pandas as pd
from utils.data_validation import (
    get_column_types,
    get_missing_values_info,
    get_duplicate_info,
    validate_data_types
)

def show_validation_wizard(df: pd.DataFrame):
    """Interactive wizard for data validation with step-by-step guidance."""
    st.subheader("Data Validation Wizard")
    st.write("Follow these steps to validate your data:")

    # Step 1: Column Types Overview
    st.write("### Step 1: Review Column Types")
    column_types = get_column_types(df)
    
    with st.expander("📊 Column Types Analysis", expanded=True):
        st.write("Here's what we detected about your columns:")
        for col, dtype in column_types.items():
            st.write(f"- {col}: {dtype}")
            if dtype == 'numeric':
                st.write(f"  📈 Range: [{df[col].min():.2f} to {df[col].max():.2f}]")
            elif dtype == 'string':
                unique_values = df[col].nunique()
                st.write(f"  📝 Unique values: {unique_values}")

    # Step 2: Missing Values Analysis
    st.write("### Step 2: Missing Values Detection")
    missing_values = get_missing_values_info(df)
    
    with st.expander("🔍 Missing Values Analysis", expanded=True):
        if any(missing_values.values()):
            st.write("Columns with missing values:")
            for col, percentage in missing_values.items():
                if percentage > 0:
                    st.write(f"- {col}: {percentage:.2f}% missing")
                    st.progress(percentage / 100)
        else:
            st.success("No missing values found in your dataset!")

    # Step 3: Duplicate Records Check
    st.write("### Step 3: Duplicate Records Check")
    num_duplicates, duplicate_indices = get_duplicate_info(df)
    
    with st.expander("🔄 Duplicate Records Analysis", expanded=True):
        if num_duplicates > 0:
            st.warning(f"Found {num_duplicates} duplicate rows")
            if st.checkbox("Show duplicate rows"):
                st.dataframe(df.iloc[duplicate_indices])
        else:
            st.success("No duplicate records found!")

    # Step 4: Data Type Validation
    st.write("### Step 4: Data Type Validation")
    validation_issues = validate_data_types(df)
    
    with st.expander("⚠️ Data Type Issues", expanded=True):
        if validation_issues:
            st.warning("Found potential data type issues:")
            for col, issues in validation_issues.items():
                st.write(f"Column '{col}':")
                for issue in issues:
                    st.write(f"  - {issue}")
        else:
            st.success("All data types are valid!")

    # Step 5: Recommendations
    st.write("### Step 5: Recommendations")
    with st.expander("💡 Recommended Actions", expanded=True):
        _show_recommendations(df, missing_values, num_duplicates, validation_issues)

def _show_recommendations(df, missing_values, num_duplicates, validation_issues):
    """Show recommended actions based on validation results."""
    recommendations = []
    
    # Missing values recommendations
    if any(v > 0 for v in missing_values.values()):
        recommendations.append({
            "title": "Handle Missing Values",
            "description": "Consider using appropriate strategies for missing values:",
            "actions": [
                "Drop rows with missing values if they represent a small portion of your data",
                "Use mean/median imputation for numerical columns",
                "Use mode imputation for categorical columns"
            ]
        })

    # Duplicate records recommendations
    if num_duplicates > 0:
        recommendations.append({
            "title": "Handle Duplicate Records",
            "description": f"Found {num_duplicates} duplicate records",
            "actions": [
                "Review duplicate rows to understand why they exist",
                "Consider removing duplicates if they're not intentional",
                "Keep duplicates if they represent legitimate repeated measurements"
            ]
        })

    # Data type issues recommendations
    if validation_issues:
        recommendations.append({
            "title": "Fix Data Type Issues",
            "description": "Some columns have data type inconsistencies",
            "actions": [
                "Review and correct non-numeric values in numeric columns",
                "Standardize date formats in datetime columns",
                "Consider converting categorical variables to appropriate types"
            ]
        })

    # Display recommendations
    if recommendations:
        for rec in recommendations:
            st.write(f"**{rec['title']}**")
            st.write(rec['description'])
            for action in rec['actions']:
                st.write(f"- {action}")
    else:
        st.success("Your data looks good! No immediate actions required.")
