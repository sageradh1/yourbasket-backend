from flask import render_template,session, request,redirect,url_for,flash
from app import app,db,login_required
from .forms import AdminLoginForm
from app.product.models import Item,Category
from app.product.productutils import getCategoriesAndItems
from app.user.models import User
from flask_login import login_user,logout_user,current_user

# @app.route('/admin/login', methods=['GET','POST'])
# def admin_login():
#     if current_user.is_authenticated and User.get_urole(current_user)=="admin":
#         return redirect(url_for('admin_home'))
#     form = AdminLoginForm()
#     if form.validate_on_submit():
#         admin = User.query.filter_by(email=form.email.data,urole="admin").first()
#         if admin and User.check_password(admin,form.password.data):
#             # session['email'] = form.email.data
#             login_user(admin)
#             admin.is_active=True
#             User.save_to_db(admin)
#             flash(f'Welcome Admin : {form.email.data} !! You are now logged in.','success')
#             return redirect(url_for('admin_home'))
#         else:
#             flash(f'Wrong email and password', 'success')
#             return redirect(url_for('admin_login'))
#     return render_template('admin/login.html',title='Login page',form=form)

@app.route('/admin/logout')
@login_required(role="admin")
def admin_logout():
    logout_user()
    return redirect(url_for('admin_home'))

@app.route('/admin/')
@login_required(role="admin")
def admin_home():
    allcategories , allitems = getCategoriesAndItems()
    return render_template('admin/index.html', title='Admin page',allcategories=allcategories , allitems=allitems)

@app.route('/categories')
@login_required(role="admin")
def admin_categories():
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html', title='categories',categories=categories)

