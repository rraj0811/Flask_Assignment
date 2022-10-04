from car_rental import db, login_manager
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView
from flask import render_template, redirect


@login_manager.user_loader
def load_user(admin_id):
    return Customers.query.get(int(admin_id))

class Controller(ModelView):
    def is_accessible(self):
        if current_user.role == 'Admin':
            return True
        

class Customers(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    address = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.Integer, unique=True, nullable = False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable = False)

    def __repr__(self):
        return f"Customers('{self.name}', '{self.email}', '{self.phone_number}')"

 
class CarDetails(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    registration_number = db.Column(db.String(100),unique=True, nullable=False)
    carname = db.Column(db.String(100), nullable = False)
    carmodel = db.Column(db.String(100),  nullable = False)
    picture = db.Column(db.String(20), nullable=False, default='default.jpg')
    is_available = db.Column(db.String(20), nullable = False)
    perhour = db.Column(db.Integer, nullable = False)
    
    # fuel_consumption = db.Column(db.Integer)
    def __repr__(self):
        return f"CarDetails('{self.registration_number}','{self.carname}', '{self.carmodel}, ')"

db.create_all()