# config/settings.py

RISK_THRESHOLDS = { # [cite: 157]
    'HIGH': 70, # [cite: 158]
    'MEDIUM': 40, # [cite: 159]
    'LOW': 0 # [cite: 160]
}

EMAIL_CONFIG = { # [cite: 162]
    'smtp_server': 'smtp.company.com', # [cite: 163]
    'port': 587, # [cite: 164]
    'username': 'hr-system@company.com', # [cite: 165]
    # 'password': 'your_email_password' # In a real app, use environment variables or a secure vault
}

SCHEDULING = { # [cite: 167]
    'daily_run_time': '09:00', # [cite: 168]
    'data_retention_days': 365 # [cite: 169]
}

ALERT_TEMPLATES = { # [cite: 61]
    "immediate_manager_alert": { # [cite: 62]
        "subject": "Employee Retention Alert - {employee_name}", # [cite: 63]
        "message": "Employee {employee_name} has been flagged as high attrition risk. Risk factors: {risk_factors}. Recommended actions: Schedule 1-on-1 meeting within 48 hours." # [cite: 64, 65]
    },
    "schedule_check_in": {
        "subject": "Employee Check-in Recommended - {employee_name}",
        "message": "Employee {employee_name} has been identified as medium attrition risk. Risk factors: {risk_factors}. Recommended actions: Schedule a check-in meeting within the next week to understand concerns."
    },
    "monitor_only": {
        "subject": "Employee Monitoring Alert - {employee_name}",
        "message": "Employee {employee_name} is currently low attrition risk but is being monitored. No immediate action required."
    }
}