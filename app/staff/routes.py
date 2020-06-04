from flask import render_template,session, request,redirect,url_for,flash
from app import app,db,login_required
from .forms import StaffRegisterForm,StaffUpdateForm
from app.product.productutils import getCategoriesAndItems
from app.staff.staffutils import getStaffs
from app.user.models import User
from flask_login import login_user,logout_user,current_user


#################### Basic staff routes ######################
@app.route('/staff/')
@login_required(role="staff")
def staff_home():
    allcategories , allitems = getCategoriesAndItems()
    return render_template('staff/index.html', title='staff page',allcategories=allcategories ,allitems=allitems)

#login is common

@app.route('/staff/logout')
@login_required(role="staff")
def staff_logout():
    
    currentuser= User.find_by_id(current_user.id)
    currentuser.is_active=False
    User.save_to_db(currentuser)
    logout_user()
    return redirect(url_for('staff_home'))
#################### Basic staff routes ######################

#################### Admin routes for operation on staffs ######################
@app.route('/admin/staffs/')
@login_required(role="admin")
def getallstaffs_admin():
    allcategories=[]
    allitems=[]
    allstaffs=[]
    try:
        allcategories , allitems = getCategoriesAndItems()
        allstaffs = getStaffs()
        return render_template('admin/staffs-all.html',allcategories=allcategories,allstaffs=allstaffs)
    except Exception as err:
        return render_template('admin/staffs-all.html',allcategories=allcategories,allstaffs=allstaffs)

@app.route('/admin/addstaff', methods=['GET','POST'])
@login_required(role="admin")
def addstaff():
    form = StaffRegisterForm()

    if request.method=="POST":
        try:
            if form.validate_on_submit():
                user = User(urole="staff",first_name=form.first_name.data,last_name=form.last_name.data,dob=form.dob.data, username=form.username.data, email=form.email.data, city=form.city.data,contactnumber=form.contactnumber.data, address=form.address.data)
                User.set_password(user,form.password.data)
                db.session.add(user)
                db.session.commit()
                flash(f'The staff with username {form.username.data} was added in database','success')
                return redirect(url_for('admin_home'))
            else:
                print(form.errors)
                return render_template('admin/staff-add.html', form=form, title='Add a staff')
        except Exception as err:
            print(err)
            return render_template('admin/staff-add.html', form=form, title='Add a staff')       
    return render_template('admin/staff-add.html', form=form, title='Add a staff')





@app.route('/updatestaff/<int:id>', methods=['GET','POST'])
@login_required(role="admin")
def updatestaff(id):
    form = StaffUpdateForm()
    user = User.query.get_or_404(id)
    if request.method=="POST":
        try:
            if form.validate_on_submit():
                user.first_name = form.first_name.data
                user.last_name = form.last_name.data
                user.dob = form.dob.data
                user.username = form.username.data
                user.email = form.email.data
                user.contactnumber = form.contactnumber.data
                user.address = form.address.data
                user.urole = "staff"
                db.session.add(user)
                db.session.commit()
                flash(f'The staff information was updated in database','success')
                return redirect(url_for('admin_home'))
            else:
                print(form.errors)
                for error in form.errors:
                    flash(form.errors[error],'warning')
                
                form = StaffUpdateForm(obj=user or None)
                return render_template('admin/staff-add.html', form=form, title='Update Staff',currentStaff=user)

        except Exception as err:
            print(err)
            form = StaffUpdateForm(obj=user or None)
            return render_template('admin/staff-add.html', form=form, title='Update Staff',currentStaff=user)

    form = StaffUpdateForm(obj=user or None)      
    return render_template('admin/staff-add.html', form=form, title='Update Staff',currentStaff=user)


@app.route('/deletestaff/<int:id>', methods=['POST'])
@login_required(role="admin")
def deletestaff(id):
    try:
        user = User.query.get_or_404(id)
        if request.method=="POST":
            db.session.delete(user)
            db.session.commit()
            flash(f"Requested staff was deleted from your database","success")
            return redirect(url_for('admin_home'))
        flash(f"Error while deleting staff","warning")
    except Exception as err:
        print(err)
        flash(f"Error while deleting staff","warning")



#################### Admin routes for operation on staffs ######################



# @app.route('/categories')
# @login_required(role="staff")
# def staff_categories():
#     categories = Category.query.order_by(Category.id.desc()).all()
#     return render_template('staff/brand.html', title='categories',categories=categories)

