from app import app
from flask import render_template,session
from app.product.models import Item,Category
from app.product.productutils import getCategoriesAndItems

@app.route('/')
def home():
    allcategories , allitems = getCategoriesAndItems()    
    return render_template('customer/home.html', allcategories=allcategories,allitems=allitems)

@app.route('/customer/login', methods=['GET','POST'])
def customer_login():
    # form = CustomerLoginFrom()
    # if form.validate_on_submit():
    #     user = Register.query.filter_by(email=form.email.data).first()
    #     if user and bcrypt.check_password_hash(user.password, form.password.data):
    #         login_user(user)
    #         flash('You are login now!', 'success')
    #         next = request.args.get('next')
    #         return redirect(next or url_for('home'))
    #     flash('Incorrect email and password','danger')
    #     return redirect(url_for('customerLogin'))
            
    # return render_template('customer/login.html', form=form)
    return 'login'

@app.route('/customer/register', methods=['GET','POST'])
def customer_register():
    # form = CustomerRegisterForm()
    # if form.validate_on_submit():
    #     hash_password = bcrypt.generate_password_hash(form.password.data)
    #     register = Register(name=form.name.data, username=form.username.data, email=form.email.data,password=hash_password,country=form.country.data, city=form.city.data,contact=form.contact.data, address=form.address.data, zipcode=form.zipcode.data)
    #     db.session.add(register)
    #     flash(f'Welcome {form.name.data} Thank you for registering', 'success')
    #     db.session.commit()
    #     return redirect(url_for('login'))
    # return render_template('customer/register.html', form=form)
    return 'register'