from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from .models import db

auth_bp = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

login_manager = LoginManager()
mail = Mail()

from . import routes  # keep this at the end to avoid circular imports