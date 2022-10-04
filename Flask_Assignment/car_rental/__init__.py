from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin






app = Flask(__name__)
# import secrets
# secrets.token_hex(16)
app.config['SECRET_KEY'] = '625da781acbd8ba3c91b3e3d08df044e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
admin = Admin(app)
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'

login_manager = LoginManager(app)
login_manager.login_view = 'landing_page'
login_manager.login_message ='Admin needs to login to access this page'
login_manager.login_message_category = 'warning'
# create db instance
# db.create_all()
from car_rental import routes


