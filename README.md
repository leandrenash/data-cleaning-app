# Data Cleaning and Processing Application

<img width="848" alt="Screenshot 2024-12-26 at 10 33 29" src="https://github.com/user-attachments/assets/86eac8b8-7650-4889-923e-96275595d6b9" />


An interactive web application built with Streamlit that simplifies data cleaning and processing tasks. This application provides an intuitive interface for users to upload, analyze, validate, and clean their datasets with minimal technical expertise required.

## Features

### 1. Data Upload and Preview
- Support for CSV and Excel file formats
- Instant preview of uploaded data
- Basic dataset information display (shape, columns, data types)
- Column statistics and value distributions

### 2. Interactive Data Validation Wizard
- Step-by-step guidance through the validation process
- Column type analysis and verification
- Missing values detection and visualization
- Duplicate records identification
- Data type consistency checking
- Smart recommendations based on data quality issues

### 3. Data Cleaning Tools
- Remove duplicate rows
- Handle missing values with multiple strategies:
  - Drop rows
  - Mean/median imputation
  - Mode imputation
  - Zero-filling
- Data type conversion
- Outlier detection and removal using IQR method

### 4. Statistical Analysis
- Missing values distribution visualization
- Numerical column distributions
- Box plots for outlier visualization
- Basic statistical measures

## Installation

1. Clone this repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```

Required packages:
- streamlit
- pandas
- plotly
- openpyxl

## Usage

1. Start the application:
```bash
streamlit run main.py
```

2. Open your web browser and navigate to the provided URL (default: http://localhost:5000)

3. Upload your data file (CSV or Excel)

4. Use the different tabs to:
   - Preview and analyze your data
   - Run the validation wizard
   - Apply cleaning operations
   - View statistical insights

5. Download your cleaned dataset when ready

## Project Structure

```
├── main.py                    # Main application file
├── .streamlit/
│   └── config.toml           # Streamlit configuration
├── components/
│   ├── data_preview.py       # Data preview functionality
│   ├── data_cleaning.py      # Data cleaning operations
│   ├── data_stats.py         # Statistical analysis
│   └── data_validation_wizard.py  # Interactive validation wizard
└── utils/
    ├── data_operations.py    # Core data operations
    └── data_validation.py    # Data validation utilities
```

## Features in Detail

### Data Validation Wizard
The wizard guides users through a comprehensive data validation process:
1. Column Types Review
2. Missing Values Detection
3. Duplicate Records Check
4. Data Type Validation
5. Recommendations

### Data Cleaning Options
- **Duplicate Removal**: Identify and remove duplicate rows
- **Missing Values**: Multiple strategies for handling missing data
- **Data Type Conversion**: Convert columns to appropriate data types
- **Outlier Removal**: Remove statistical outliers using IQR method

### Statistical Analysis
- Visualize data distributions
- Identify patterns and anomalies
- Understand data quality issues

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details
