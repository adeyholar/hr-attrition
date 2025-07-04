import sys
import os

# Add the config directory to the Python path to import settings
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config')))
import settings

def send_alert_email(recipient_email, employee_name, risk_factors, action_template_name):
    """
    Simulates sending an email notification to a manager or HR. [cite: 56]
    In a real application, this would use Python's smtplib.
    """
    template = settings.ALERT_TEMPLATES.get(action_template_name) # [cite: 61]
    if not template:
        print(f"Error: No template found for action '{action_template_name}'")
        return False

    subject = template['subject'].format(employee_name=employee_name) # [cite: 63]
    message = template['message'].format(employee_name=employee_name, risk_factors=risk_factors) # [cite: 64, 65]

    print(f"\n--- Sending Email ---")
    print(f"To: {recipient_email}")
    print(f"From: {settings.EMAIL_CONFIG['username']}") # [cite: 165]
    print(f"Subject: {subject}")
    print(f"Message:\n{message}")
    print(f"--- Email Sent (Simulated) ---\n")
    # In a real application:
    # try:
    #     import smtplib
    #     from email.mime.text import MIMEText
    #     msg = MIMEText(message)
    #     msg['Subject'] = subject
    #     msg['From'] = settings.EMAIL_CONFIG['username']
    #     msg['To'] = recipient_email
    #
    #     with smtplib.SMTP(settings.EMAIL_CONFIG['smtp_server'], settings.EMAIL_CONFIG['port']) as server:
    #         server.starttls()
    #         # server.login(settings.EMAIL_CONFIG['username'], settings.EMAIL_CONFIG['password']) # Password would be from a secure config
    #         server.send_message(msg)
    #     print(f"Email sent successfully to {recipient_email}")
    #     return True
    # except Exception as e:
    #     print(f"Failed to send email: {e}")
    #     return False
    return True # Always return True for simulation

if __name__ == '__main__':
    # Example Usage:
    manager_email = "manager1@company.com"
    employee_name = "John Doe"
    risk_factors = "Tenure (new), Low Performance, High Absences"
    action_type = "immediate_manager_alert" # [cite: 62]

    send_alert_email(manager_email, employee_name, risk_factors, action_type)

    # Example of an unrecognized action type
    send_alert_email("hr@company.com", "Jane Smith", "No specific risk", "unknown_action")