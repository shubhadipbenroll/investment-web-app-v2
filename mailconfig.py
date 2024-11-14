# mailconfig.py

import base64
from io import BytesIO
import re
from flask_mail import Mail, Message
from flask import Flask

# Email sending setup function
def configure_mail(app):
    # Configuration for Flask-Mail
    """app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'test@gmail.com'  # Your email address
    app.config['MAIL_PASSWORD'] = 'test2023'          # Your email password or app password
    app.config['MAIL_DEFAULT_SENDER'] = 'test@gmail.com'  # Your email address"""

    app.config['MAIL_SERVER'] = 'mail.investinbulls.net'  # HostGator mail server
    app.config['MAIL_PORT'] = 465  # SMTP Port for SSL
    app.config['MAIL_USE_SSL'] = True  # Enable SSL as required by HostGator
    app.config['MAIL_USE_TLS'] = False  # SSL used instead of TLS
    app.config['MAIL_USERNAME'] = 'alerts@investinbulls.net'  # Your HostGator email address
    app.config['MAIL_PASSWORD'] = 'I!nvest!nbulls123'  # Your email password (use environment variable in production)
    app.config['MAIL_DEFAULT_SENDER'] = 'alerts@investinbulls.net'  # Default sender email address

    
    mail = Mail(app)
    return mail

# Function to send an email
def send_email(mail, to_email, subject, message_body):
    try:
        msg = Message(subject, recipients=[to_email])
        msg.body = message_body
        mail.send(msg)
        return "Email sent successfully!"
    except Exception as e:
        return str(e)

def send_email_to_users(mail, to_email, subject, message_body):
    try:
        msg = Message(subject, recipients=[to_email])
        msg.html = message_body  # Use HTML for rich content with images and formatted text
        # Extract base64 images and attach them with cid
        base64_images = re.findall(r'data:image/(png|jpeg);base64,([^\"]+)', message_body)
        for idx, (img_type, img_data) in enumerate(base64_images):
            image_data = base64.b64decode(img_data)
            img_filename = f'image_{idx}.{img_type}'
            
            # Attach image with Content-ID for inline use
            msg.attach(img_filename, f'image/{img_type}', image_data, headers={"Content-ID": f"<img{idx}>"})
            
            # Replace base64 src in the HTML content with cid reference
            msg.html = msg.html.replace(f'data:image/{img_type};base64,{img_data}', f'cid:img{idx}')

        mail.send(msg)
        return "Email sent successfully!"
    except Exception as e:
        return str(e)
