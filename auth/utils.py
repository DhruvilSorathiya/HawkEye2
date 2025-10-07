from flask_mail import Message
from flask import url_for, current_app
from itsdangerous import URLSafeTimedSerializer
import bcrypt
from datetime import datetime, timedelta
import secrets

def send_reset_email(user, token, mail):
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    msg = Message('Password Reset Request',
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{reset_url}

If you did not make this request, simply ignore this email.
'''
    mail.send(msg)

def generate_token():
    return secrets.token_urlsafe(32)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(hashed, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def token_expiry(hours=2):
    return datetime.utcnow() + timedelta(hours=hours)