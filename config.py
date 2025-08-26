import os

# Email configuration with environment variables for production
EMAIL_CONFIG = {
    'smtp_server': os.environ.get('EMAIL_SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.environ.get('EMAIL_SMTP_PORT', 587)),
    'sender_email': os.environ.get('EMAIL_SENDER', 'your-email@gmail.com'),
    'sender_password': os.environ.get('EMAIL_PASSWORD', 'your-app-password')
}

# Instructions to set up Gmail App Password:
# 1. Go to your Google Account settings
# 2. Security → 2-Step Verification (enable if not already)
# 3. Security → App passwords
# 4. Generate app password for "Mail"
# 5. Use that password here (not your regular Gmail password)