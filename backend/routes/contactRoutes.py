from flask import Blueprint, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

contact_bp = Blueprint('contact_bp', __name__)

# Set your email credentials here or use environment variables
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USER = os.getenv('CONTACT_EMAIL_USER', 'pcyc323@gmail.com')
EMAIL_PASS = os.getenv('CONTACT_EMAIL_PASS', 'CONTACT_EMAIL_PASS')  # Use an app password for Gmail
TO_EMAIL = 'pcyc323@gmail.com'

@contact_bp.route('/contact', methods=['POST'])
def send_contact_email():
    data = request.json
    name = data.get('name', 'Anonymous')
    email = data.get('email', '')
    message = data.get('message', '')
    if not email or not message:
        return jsonify({'error': 'Email and message are required.'}), 400
    subject = f"Contact Form Message from {name} ({email})"
    body = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = TO_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, TO_EMAIL, msg.as_string())
        server.quit()
        return jsonify({'success': True, 'message': 'Email sent successfully.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
