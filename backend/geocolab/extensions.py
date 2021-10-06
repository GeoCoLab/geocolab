from flask_mail import Mail
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()
crypt = CryptContext(schemes=['argon2'], deprecated='auto')
csrf = CSRFProtect()
