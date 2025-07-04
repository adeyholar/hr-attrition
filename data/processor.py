import pandas as pd

def ingest_data(file_path):
    """
    Ingests employee data from a CSV file.
    In a real-world scenario, this would involve more robust data pulling from a database.
    """
    try:
        df = pd.read_csv(file_path)
        print(f"Successfully ingested data from {file_path}. Rows: {len(df)}")
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return pd.DataFrame() # Return an empty DataFrame on error

def clean_data(df):
    """
    Performs basic data cleaning and validation.
    - Fills missing values for numerical columns with 0.
    - Converts 'hire_date' to datetime objects.
    """
    print("Cleaning data...")
    # Fill potential missing numerical values with 0 (e.g., performance_score, absence_days)
    numerical_cols = ['performance_score', 'absence_days_30d', 'absence_days_90d'] # Assuming these columns exist in the CSV example [cite: 13]
    for col in numerical_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    # Convert hire_date to datetime objects
    if 'hire_date' in df.columns:
        df['hire_date'] = pd.to_datetime(df['hire_date'], errors='coerce')
        # Drop rows where hire_date could not be parsed
        df.dropna(subset=['hire_date'], inplace=True)

    print("Data cleaning complete.")
    return df

def feature_engineering(df):
    """
    Calculates tenure in months and a simplified performance trend.
    """
    print("Performing feature engineering...")
    if 'hire_date' in df.columns:
        df['tenure_months'] = ((pd.to_datetime('now') - df['hire_date']).dt.days / 30).astype(int)
    else:
        df['tenure_months'] = 0 # Default if hire_date is missing

    # Simplified performance trend: if performance_score is low, assume declining for this example
    # In a real system, this would compare current performance to past reviews [cite: 10, 22]
    if 'performance_score' in df.columns:
        df['performance_trend'] = df['performance_score'].apply(lambda x: 'declining' if x < 2.5 else 'improving/stable')
    else:
        df['performance_trend'] = 'unknown'

    print("Feature engineering complete.")
    return df

if __name__ == '__main__':
    # Example Usage:
    sample_csv_path = 'sample_employee_data.csv' # This file needs to exist in the 'data/' directory [cite: 73]
    # Create a dummy CSV for testing
    dummy_data = {
        'employee_id': ['EMP001', 'EMP002', 'EMP003', 'EMP004'],
        'name': ['John Doe', 'Jane Smith', 'Peter Jones', 'Alice Brown'],
        'department': ['Engineering', 'HR', 'Sales', 'Engineering'],
        'manager_email': ['manager1@company.com', 'manager2@company.com', 'manager3@company.com', 'manager1@company.com'],
        'hire_date': ['2024-01-15', '2020-03-10', '2023-06-01', '2019-11-20'],
        'performance_score': [3.2, 2.0, 4.1, 2.8],
        'absence_days_30d': [2, 5, 1, 0],
        'absence_days_90d': [8, 15, 3, 2]
    }
    dummy_df = pd.DataFrame(dummy_data)
    dummy_df.to_csv(sample_csv_path, index=False)

    employee_df = ingest_data(sample_csv_path)
    if not employee_df.empty:
        cleaned_df = clean_data(employee_df)
        processed_df = feature_engineering(cleaned_df)
        print("\nProcessed Data Sample:")
        print(processed_df.head())