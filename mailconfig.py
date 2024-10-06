# mailconfig.py

from flask import Flask
from flask_mail import Mail

# Create a Flask application instance
app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'shubhadip.bera.2023@gmail.com'  # Your email address
app.config['MAIL_PASSWORD'] = 'abcd1234'          # Your email password or app password
app.config['MAIL_DEFAULT_SENDER'] = 'shubhadip.bera.2023@gmail.com'  # Your email address

# Initialize the Mail instance
mail = Mail(app)
