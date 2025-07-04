import sys
import os

# Add the config directory to the Python path to import settings
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config')))
import settings

def decide_action(employee_data, risk_score):
    """
    Decides the appropriate action based on the calculated risk score. [cite: 47]
    Uses risk thresholds defined in settings. [cite: 157, 158, 159, 160]
    """
    if risk_score >= settings.RISK_THRESHOLDS['HIGH']: # [cite: 42, 48]
        return "immediate_manager_alert" # [cite: 49]
    elif risk_score >= settings.RISK_THRESHOLDS['MEDIUM']: # [cite: 43, 50]
        return "schedule_check_in" # [cite: 51]
    else: # [cite: 44, 52]
        return "monitor_only" # [cite: 53]

if __name__ == '__main__':
    # Example Usage:
    # Assuming a sample employee_data dictionary (not directly used in decision but good for context)
    sample_employee_data = {'employee_id': 'EMP001', 'name': 'John Doe'}

    # Test cases for decision logic
    risk_score_high = 80
    action_high = decide_action(sample_employee_data, risk_score_high)
    print(f"Risk score: {risk_score_high}, Recommended action: {action_high}") # Expected: immediate_manager_alert

    risk_score_medium = 55
    action_medium = decide_action(sample_employee_data, risk_score_medium)
    print(f"Risk score: {risk_score_medium}, Recommended action: {action_medium}") # Expected: schedule_check_in

    risk_score_low = 25
    action_low = decide_action(sample_employee_data, risk_score_low)
    print(f"Risk score: {risk_score_low}, Recommended action: {action_low}") # Expected: monitor_only