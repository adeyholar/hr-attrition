def calculate_risk_score(employee_data):
    """
    Calculates a risk score for an employee based on tenure, performance, and absence.
    Score is capped at 100. [cite: 28, 39]
    """
    risk_score = 0

    # Tenure risk (higher risk for new and very long tenure) [cite: 29]
    if employee_data['tenure_months'] < 6:
        risk_score += 30 # [cite: 30, 31]
    elif employee_data['tenure_months'] > 60:
        risk_score += 20 # [cite: 32, 33]

    # Performance risk [cite: 34]
    if employee_data['performance_score'] < 2.5:
        risk_score += 40 # [cite: 35, 36]

    # Absence risk [cite: 37]
    if employee_data['absence_days_30d'] > 3:
        risk_score += 20 # [cite: 38]

    return min(risk_score, 100) # [cite: 39]

if __name__ == '__main__':
    # Example Usage:
    sample_employee = {
        'employee_id': 'EMP001',
        'name': 'John Doe',
        'tenure_months': 5, # High risk due to new tenure [cite: 30]
        'performance_score': 2.0, # High risk due to low performance [cite: 35]
        'absence_days_30d': 4 # High risk due to absences [cite: 38]
    }
    risk = calculate_risk_score(sample_employee)
    print(f"Employee {sample_employee['name']} has a risk score of: {risk}") # Expected: 30 + 40 + 20 = 90

    sample_employee_2 = {
        'employee_id': 'EMP002',
        'name': 'Jane Smith',
        'tenure_months': 30,
        'performance_score': 3.5,
        'absence_days_30d': 1
    }
    risk_2 = calculate_risk_score(sample_employee_2)
    print(f"Employee {sample_employee_2['name']} has a risk score of: {risk_2}") # Expected: 0