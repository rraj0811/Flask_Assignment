import os
import secrets
from flask import render_template,url_for,flash, redirect, request
from car_rental import app, bcrypt, db, admin
from car_rental.forms import CustomerRegistrationForm, LoginForm,  ForgotPassword, CarDetailsForm, CostCalculationForm, SearchForm
from car_rental.models import  Customers, CarDetails, Controller
from flask_login import login_user, current_user, logout_user, login_required
import phonenumbers


admin.add_view(Controller(Customers,db.session))
admin.add_view(Controller(CarDetails,db.session))




#phone number extraction from parsed num
def full_phone(formnum):
    my_string_number = formnum
    #my_number = phonenumbers.parse(my_string_number)
    ph_str = str(my_string_number)
    sp_chr = ph_str.split(' ')
    num_str = ''
    for chr in sp_chr:
        try:
            num = int(chr)
            num_str += chr
        except:
            continue
    return int(num_str)


#db.create_all()

@app.route('/',methods=['GET','POST'])
def landing_page():
   
    form = LoginForm()
    if form.validate_on_submit():
        user = Customers.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            if user.role == 'Admin' :
                return redirect(url_for('admin'))
            elif user.role == 'User':
                return redirect(url_for('home'))
            
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('landing_page.html', title='Landing Page', form = form)




@app.route('/admin/')
@login_required
def admin():
    return render_template('index.html')


@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/forgot_password', methods = ['GET','POST'])
def forgot_password():
    form = ForgotPassword()
    if form.validate_on_submit():
        user = Customers.query.filter_by(username=form.username.data).first()
        if user:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            Customers.password = hashed_password
            db.session.commit()
            flash(f'Your password has been changed successfully!', 'success')
            return redirect(url_for('landing_page'))
        else:
            flash(f"User doen't exists", 'danger')
    return render_template('forgot_password.html', title = 'Forgot Password' , form = form)

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = CustomerRegistrationForm()
    if form.validate_on_submit():
        if form.phone_number.data:
            try:
                phone_number_with_country_code = phonenumbers.parse("+"+form.phone_number.data)
                full_num = full_phone(phone_number_with_country_code)
            except:
                phone_number_with_country_code = phonenumbers.parse("+91"+form.phone_number.data)
                full_num = full_phone(phone_number_with_country_code)

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Customers(name = form.name.data, email = form.email.data, phone_number=full_num, address=form.address.data,
                            username = form.username.data, password = hashed_password, role = form.role.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! Your now able to log in', 'success')
        return redirect(url_for('landing_page'))
    return render_template('register.html', title = 'Register', form = form)
    

@app.route('/customer_register', methods=['GET','POST'])
@login_required
def customer_register():
    if not current_user.is_authenticated:
        return redirect(url_for('landing_page'))
    form = CustomerRegistrationForm()           
    if form.validate_on_submit():
        if form.phone_number.data:
            try:
                phone_number_with_country_code = phonenumbers.parse("+"+form.phone_number.data)
                full_num = full_phone(phone_number_with_country_code)
            except:
                phone_number_with_country_code = phonenumbers.parse("+91"+form.phone_number.data)
                full_num = full_phone(phone_number_with_country_code)
        user = Customers(name = form.name.data, email = form.email.data, phone_number=full_num, address=form.address.data)
       
        db.session.add(user)
        db.session.commit()
        flash(f'Customer has been Registered Successfully', 'success')
        return redirect(url_for('home'))
    return render_template('customer_register.html', title = 'Customer Register', form = form)





@app.route('/cardetails', methods=['GET', 'POST'])
@login_required
def cardetails():
    posts= CarDetails.query.all()
    form = SearchForm()
    if form.validate_on_submit():
        return redirect((url_for('search_results', query=form.search.data)))
    return render_template('cardetails.html',posts=posts, form = form)

@app.route('/search_results/<string:query>')
@login_required
def search_results(query):
    form = SearchForm()
    search = "%{}%".format(query)
    records = CarDetails.query.filter(CarDetails.carname.like(search)).all()
    return render_template('search.html',  posts=records, form = form)
    # if form.validate_on_submit():
    #     return redirect((url_for('search_results', query=form.search.data)))

@app.route('/image/<string:filepath>', methods=['GET','POST'])
@login_required
def view_image(filepath):
    image_file = url_for('static', filename='car_pics/' + filepath)
    return render_template('cardetails.html', image_file = image_file, url = '/image/'+filepath)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/car_pics', picture_fn)
    form_picture.save(picture_path)

    return picture_fn


@app.route('/upload_car_details', methods=['GET', 'POST'])
@login_required
def upload_car_details():
    form = CarDetailsForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
        else:
            picture_file = 'default.jpg'
        car = CarDetails(registration_number = form.registration_number.data, carname = form.carname.data, carmodel = form.carmodel.data, picture = picture_file)
        db.session.add(car)
        db.session.commit()
        flash(f'Car details uploaded successfully', 'success')
        return redirect(url_for('home'))
  
    return render_template('cardetails.html', title = 'Upload Car Details', form = form)


@app.route('/book/<string:registration_number>', methods = ['GET','POST'])
@login_required
def book(registration_number):
    record = CarDetails.query.filter_by(registration_number = registration_number).first()
    if record.is_available == 'Yes':
        form = CostCalculationForm()
        if form.validate_on_submit():
            form.amount.data = int(form.hours.data) * record.perhour
        return render_template('cost.html', form = form)





@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('landing_page'))
 





