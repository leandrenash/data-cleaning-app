import logging
import sys
import zipfile
import io

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    logger.info("Importing streamlit...")
    import streamlit as st
    logger.info("Importing pandas...")
    import pandas as pd
    logger.info("Importing components...")
    from utils.data_operations import load_data
    from components.data_preview import show_data_preview, show_column_statistics
    from components.data_cleaning import show_cleaning_options
    from components.data_stats import show_data_statistics
    from components.data_validation_wizard import show_validation_wizard
except Exception as e:
    logger.error(f"Error during imports: {str(e)}")
    sys.exit(1)

def create_code_zip():
    """Create a zip file containing all the Python scripts."""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add main script
        zip_file.write('main.py')
        # Add utility scripts
        zip_file.write('utils/data_operations.py', 'utils/data_operations.py')
        zip_file.write('utils/data_validation.py', 'utils/data_validation.py')
        # Add component scripts
        zip_file.write('components/data_preview.py', 'components/data_preview.py')
        zip_file.write('components/data_cleaning.py', 'components/data_cleaning.py')
        zip_file.write('components/data_stats.py', 'components/data_stats.py')
        zip_file.write('components/data_validation_wizard.py', 'components/data_validation_wizard.py')
        # Add configuration
        zip_file.write('.streamlit/config.toml', '.streamlit/config.toml')
        # Add requirements info
        requirements = """
streamlit
pandas
plotly
openpyxl
        """
        zip_file.writestr('requirements.txt', requirements.strip())
    return zip_buffer

def main():
    try:
        st.set_page_config(
            page_title="Data Cleaning App",
            page_icon="📊",
            layout="wide"
        )

        st.title("Data Cleaning and Processing App")
        st.write("Upload your data file and clean it according to your preferences")

        # Add download code button in the sidebar
        with st.sidebar:
            st.write("### Download Application Code")
            st.write("Get the complete source code of this application:")
            zip_buffer = create_code_zip()
            st.download_button(
                label="Download Source Code",
                data=zip_buffer.getvalue(),
                file_name="data_cleaning_app.zip",
                mime="application/zip"
            )

        # File upload
        uploaded_file = st.file_uploader(
            "Choose a CSV or Excel file",
            type=['csv', 'xlsx', 'xls']
        )

        if uploaded_file is not None:
            # Load data
            logger.info(f"Loading file: {uploaded_file.name}")
            data = load_data(uploaded_file)

            if isinstance(data, str):
                st.error(data)
                return

            # Store original data in session state
            if 'original_data' not in st.session_state:
                st.session_state.original_data = data.copy()

            # Create tabs for different sections
            tab1, tab2, tab3, tab4 = st.tabs([
                "Data Preview",
                "Validation Wizard",
                "Data Cleaning",
                "Statistics"
            ])

            with tab1:
                show_data_preview(data)
                show_column_statistics(data)

            with tab2:
                show_validation_wizard(data)

            with tab3:
                cleaned_data = show_cleaning_options(data)

                if cleaned_data is not None:
                    st.subheader("Cleaned Data Preview")
                    st.dataframe(cleaned_data.head())

                    # Download button for cleaned data
                    csv = cleaned_data.to_csv(index=False)
                    st.download_button(
                        label="Download Cleaned Data",
                        data=csv,
                        file_name="cleaned_data.csv",
                        mime="text/csv"
                    )

            with tab4:
                show_data_statistics(data)

    except Exception as e:
        logger.error(f"Error in main function: {str(e)}")
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()