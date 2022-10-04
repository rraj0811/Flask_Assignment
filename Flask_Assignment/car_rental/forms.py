from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError 
from car_rental.models import Customers, CarDetails
from flask_admin.form import ImageUploadField, FileUploadInput, FileUploadField
import phonenumbers


class LoginForm(FlaskForm):
    username = StringField('Username',
                        validators=[DataRequired(), Length(min=2, max=20)])                        
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



class ForgotPassword(FlaskForm):
    username = StringField('User name', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')


class CustomerRegistrationForm(FlaskForm):

    name = StringField('Name', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', 
                                validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired(), Length(min=2 , max=200)])
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])
    role = StringField('Role', 
                            validators=[DataRequired(), Length(min=2, max=20)])

    submit = SubmitField('Register')
    
    #Custom Validators
    def validate_name(self,name):
       user =  Customers.query.filter_by(name = name.data).first()
       if user:
            raise ValidationError('This user is already registered')
    
    def validate_email(self, email):
       user =  Customers.query.filter_by(email = email.data).first()
       if user:
            raise ValidationError('This email is taken Please choose a different one')
        
    def validate_phone_number(self,phone_number):
        user =  Customers.query.filter_by(phone_number=phone_number.data).first()
        if user:
            raise ValidationError('Phone Number already exists.')
        if len(phone_number.data) > 12 :
            raise ValidationError('Invalid phone number.')
        try:
            input_number = phonenumbers.parse(phone_number.data)
            if not (phonenumbers.is_possible_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            input_number = phonenumbers.parse("+91"+phone_number.data)
            if not (phonenumbers.is_possible_number(input_number)):
                raise ValidationError('Invalid phone number.')

    def validate_username(self, username):
        user = Customers.query.filter_by(username = username.data).first()
        if user :
            raise ValidationError("Username already exists! Try with different Username")
    
    def validate_role(self, role):
        if role.data not in ['Admin','User'] :
            raise ValidationError("Please enter valid role either Admin or User")
        


class CarDetailsForm(FlaskForm):
    registration_number = StringField('Registration Number',
                                        validators=[DataRequired(), Length(min=2, max=20)])
    carname = StringField('Car Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    carmodel = StringField('Car Model',
                        validators=[DataRequired(), Length(min=2, max=20)])
    picture = FileUploadInput()#'Upload Picture', 
                                    #validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Register')
    
    def __repr__(self):
        return f"CarDetails('{self.registration_number}','{self.carname}', '{self.carmodel}')"

    def validate_registration_number(self,  registration_number):
        user = CarDetails.query.filter_by(registration_number = registration_number.data).first()
        if user:
            raise ValidationError('Registration Number Already Exists')

class CostCalculationForm(FlaskForm):
    hours = StringField('Hours', validators=[DataRequired()])
    amount = FloatField('Amount')
    submit = SubmitField('Book')

    def validate_hours(self, hours):
        try :
            int(hours)
        except ValueError:
            raise ValidationError('hours must be in integers')



class SearchForm(FlaskForm):
  search = StringField(render_kw={"placeholder": "Search"})
  submit = SubmitField('Search')

# import os.path as op
# from flask_admin.form import BaseForm
# from flask_admin.form.upload import ImageUploadField, secure_filename

# def thumb_name(filename):
#     name, _ = op.splitext(filename)
#     return secure_filename('%s-thumb.jpg' % name)

# class MyForm(BaseForm):
#     upload = ImageUploadField('File', thumbgen=thumb_name)





