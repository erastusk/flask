from flask import Flask
from  flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager





app  = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = 'YOUR_RECAPTCHA_PUBLIC_KEY'
app.config['RECAPTCHA_PRIVATE_KEY'] = 'YOUR_RECAPTCHA_PRIVATE_KEY'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from weather import routes
