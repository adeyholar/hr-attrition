import pandas as pd
import datetime
import os
import sqlite3

# Import modules from respective directories
from data import processor
from models import risk_calculator, decision_engine
from actions import email_handler
from config import settings # Import settings for daily_run_time

def initialize_database(db_name="employee_attrition.db"):
    """
    Initializes SQLite database with necessary tables if they don't exist.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create employees table [cite: 85]
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id TEXT PRIMARY KEY, [cite: 88]
        name TEXT, [cite: 89]
        department TEXT, [cite: 90]
        manager_email TEXT, [cite: 91]
        hire_date DATE, [cite: 92]
        current_performance REAL, [cite: 93]
        status TEXT [cite: 94]
    );
    """)

    # Create risk_assessments table [cite: 95]
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS risk_assessments (
        id INTEGER PRIMARY KEY, [cite: 97]
        employee_id TEXT, [cite: 98]
        assessment_date DATE, [cite: 99]
        risk_score INTEGER, [cite: 100]
        risk_factors TEXT, [cite: 101]
        action_taken TEXT, [cite: 102]
        FOREIGN KEY (employee_id) REFERENCES employees (id) [cite: 103]
    );
    """)

    # Create actions_log table [cite: 105]
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS actions_log (
        id INTEGER PRIMARY KEY, [cite: 107]
        employee_id TEXT, [cite: 108]
        action_type TEXT, [cite: 109]
        action_date DATE, [cite: 110]
        status TEXT, [cite: 111]
        manager_response TEXT [cite: 112]
    );
    """)
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def update_employee_in_db(employee_df, db_name="employee_attrition.db"):
    """
    Updates or inserts employee data into the database.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    for index, row in employee_df.iterrows():
        cursor.execute("""
            INSERT OR REPLACE INTO employees (id, name, department, manager_email, hire_date, current_performance, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (row['employee_id'], row['name'], row['department'], row['manager_email'],
              row['hire_date'].strftime('%Y-%m-%d'), row['performance_score'], 'Active')) # Assuming 'Active' status
    conn.commit()
    conn.close()
    print(f"Updated {len(employee_df)} employees in the database.")


def log_risk_assessment(employee_id, risk_score, risk_factors, action_taken, db_name="employee_attrition.db"):
    """
    Logs each risk assessment to the database. [cite: 95]
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    assessment_date = datetime.date.today().strftime('%Y-%m-%d')
    cursor.execute("""
        INSERT INTO risk_assessments (employee_id, assessment_date, risk_score, risk_factors, action_taken)
        VALUES (?, ?, ?, ?, ?)
    """, (employee_id, assessment_date, risk_score, risk_factors, action_taken))
    conn.commit()
    conn.close()

def log_action(employee_id, action_type, status, manager_response="", db_name="employee_attrition.db"):
    """
    Logs actions taken to the database. [cite: 105]
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    action_date = datetime.date.today().strftime('%Y-%m-%d')
    cursor.execute("""
        INSERT INTO actions_log (employee_id, action_type, action_date, status, manager_response)
        VALUES (?, ?, ?, ?, ?)
    """, (employee_id, action_type, action_date, status, manager_response))
    conn.commit()
    conn.close()


def daily_execution_cycle(data_source_path="data/sample_employee_data.csv"):
    """
    Orchestrates the daily execution cycle of the attrition prevention agent. [cite: 115]
    """
    print(f"--- Daily Execution Cycle Started: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")

    # 1. Data Collection (Simulated at 9:00 AM) [cite: 116]
    print("\n1. Data Collection (Pulling latest employee data...)") # [cite: 117]
    employee_df = processor.ingest_data(data_source_path)
    if employee_df.empty:
        print("No data ingested. Exiting daily cycle.")
        return

    cleaned_df = processor.clean_data(employee_df.copy())
    processed_df = processor.feature_engineering(cleaned_df.copy())
    update_employee_in_db(processed_df) # Update DB with latest employee info and calculated features

    # 2. Risk Assessment (Simulated at 9:30 AM) [cite: 121]
    print("\n2. Risk Assessment (Calculating risk scores...)") # [cite: 124]
    for index, employee in processed_df.iterrows():
        risk_score = risk_calculator.calculate_risk_score(employee.to_dict())
        employee_id = employee['employee_id']
        employee_name = employee['name']

        # Construct risk factors string for logging and emails
        risk_factors_list = []
        if employee['tenure_months'] < 6:
            risk_factors_list.append("New Tenure (<6 months)")
        elif employee['tenure_months'] > 60:
            risk_factors_list.append("Long Tenure (>60 months)")
        if employee['performance_score'] < 2.5:
            risk_factors_list.append("Low Performance (<2.5)")
        if employee['absence_days_30d'] > 3:
            risk_factors_list.append("High Absences (>3 days in 30d)")
        risk_factors_str = ", ".join(risk_factors_list) if risk_factors_list else "None identified"

        # 3. Decision Making (Simulated at 10:00 AM) [cite: 127]
        action_type = decision_engine.decide_action(employee.to_dict(), risk_score) # [cite: 128]
        print(f"  - Employee: {employee_name} (Score: {risk_score}) -> Action: {action_type}")

        log_risk_assessment(employee_id, risk_score, risk_factors_str, action_type)

        # 4. Action Execution (Simulated at 10:15 AM) [cite: 129]
        if action_type == "immediate_manager_alert": # [cite: 49]
            email_handler.send_alert_email(employee['manager_email'], employee_name, risk_factors_str, action_type) # [cite: 130]
            log_action(employee_id, action_type, "Email Sent")
        elif action_type == "schedule_check_in": # [cite: 51]
            # In a real scenario, this would trigger scheduler.py [cite: 82]
            print(f"  - Action: Automated scheduling request for check-in for {employee_name}")
            email_handler.send_alert_email(employee['manager_email'], employee_name, risk_factors_str, action_type)
            log_action(employee_id, action_type, "Scheduled (Simulated)")
        elif action_type == "monitor_only": # [cite: 53]
            print(f"  - Action: Monitoring only for {employee_name}")
            log_action(employee_id, action_type, "Monitored")

    # 5. Monitoring (Throughout day - simulated by log review) [cite: 133]
    print("\n5. Monitoring (Review logs and dashboard for tracking)") # [cite: 134]

    print(f"--- Daily Execution Cycle Finished: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")


if __name__ == '__main__':
    # Ensure the 'data' directory exists
    os.makedirs('data', exist_ok=True)

    # Create a dummy CSV for testing if it doesn't exist
    sample_csv_path = 'data/sample_employee_data.csv'
    if not os.path.exists(sample_csv_path):
        dummy_data = {
            'employee_id': ['EMP001', 'EMP002', 'EMP003', 'EMP004', 'EMP005', 'EMP006'],
            'name': ['John Doe', 'Jane Smith', 'Peter Jones', 'Alice Brown', 'Bob White', 'Charlie Green'],
            'department': ['Engineering', 'HR', 'Sales', 'Engineering', 'Marketing', 'HR'],
            'manager_email': ['manager1@company.com', 'manager2@company.com', 'manager3@company.com', 'manager1@company.com', 'manager4@company.com', 'manager2@company.com'],
            'hire_date': ['2024-06-15', '2020-03-10', '2023-01-01', '2019-11-20', '2024-05-01', '2015-07-01'],
            'performance_score': [2.1, 3.8, 4.0, 2.5, 1.9, 3.2],
            'absence_days_30d': [4, 1, 0, 2, 5, 1],
            'absence_days_90d': [10, 3, 1, 5, 12, 4]
        }
        dummy_df = pd.DataFrame(dummy_data)
        dummy_df.to_csv(sample_csv_path, index=False)
        print(f"Created dummy data file: {sample_csv_path}")

    initialize_database()
    daily_execution_cycle(data_source_path=sample_csv_path)

    print("\nTo inspect the database, you can use a SQLite browser on 'employee_attrition.db'.")