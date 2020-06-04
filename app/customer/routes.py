from app import app,db,login_required
from app.product.models import Item,Category
from app.product.productutils import getCategoriesAndItems
from .forms import CustomerRegisterForm
from app.user.models import User
from flask import render_template,session,flash,request,redirect,url_for
from flask_login import current_user, logout_user, login_user

@app.route('/')
def customer_home():
    allcategories , allitems = getCategoriesAndItems()    
    return render_template('customer/home.html', allcategories=allcategories,allitems=allitems)

@app.route('/aboutus')
def about_us():
    allcategories , allitems = getCategoriesAndItems()    
    return render_template('customer/about-us.html', allcategories=allcategories,allitems=allitems)
# @app.route('/customer/login', methods=['GET','POST'])
# def customer_login():
#     if current_user.is_authenticated:
#         flash("You will have to logout first ! ",'danger')
#         return redirect(url_for('home'))

#     allcategories , allitems = getCategoriesAndItems() 
#     form = CustomerLoginForm()
#     if form.validate_on_submit():
#         try:
#             user = User.query.filter_by(username=form.username.data,urole="customer").first()
#             if user and User.check_password(user,form.password.data):
#                 login_user(user)
#                 flash('You are now logged in!', 'success')
#                 next = request.args.get('next')
#                 return redirect(next or url_for('home'))
#             flash('Incorrect email and password','danger')
#             return redirect(url_for('customer_login'))
#         except Exception as err:
#             print(err)
#             flash('Problem while logging','danger')
#             return redirect(url_for('customer_login'))            
            
#     return render_template('customer/login.html', form=form,allcategories=allcategories,allitems=allitems)


@app.route('/customer/register', methods=['GET','POST'])
def customer_register():
    if current_user.is_authenticated:
        flash("You will have to logout first ! ",'danger')
        return redirect(url_for('customer_home'))

    allcategories , allitems = getCategoriesAndItems()
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        try:
            user = User(first_name=form.first_name.data,last_name=form.last_name.data,dob=form.dob.data, username=form.username.data, email=form.email.data, city=form.city.data,contactnumber=form.contactnumber.data, address=form.address.data)
            User.set_password(user,form.password.data)
            db.session.add(user)
            flash(f'Welcome {form.first_name.data}!! Thank you for registering', 'success')
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as err:
            print(err)
            flash('Problem while registering','danger')
            return redirect(url_for('login'))

    return render_template('customer/register.html', form=form,allcategories=allcategories,allitems=allitems)


@app.route('/customer/logout')
@login_required(role="customer")
def customer_logout():
    
    currentuser= User.query.get_or_404(current_user.id)
    currentuser.is_user_active=False
    User.save_to_db(currentuser)
    logout_user()
    return redirect(url_for('customer_home'))