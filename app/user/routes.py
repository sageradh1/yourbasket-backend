from app import app
from flask_login import current_user,login_user
from flask import flash,redirect,url_for,render_template
from .models import User
from .forms import LoginForm

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated and User.get_urole(current_user)=="admin":
        flash("You will have to logout first ! ",'danger')
        return redirect(url_for('admin_home'))
    if (current_user.is_authenticated and current_user.urole=="customer"):
        flash("You will have to logout first ! ",'danger')
        return redirect(url_for('customer_home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            if User.check_password(user,form.password.data):
                login_user(user)
                user.is_active=True
                User.save_to_db(user)


                if user.urole=="admin":
                    flash(f'Welcome Admin!! You are now logged in.','success')
                    return redirect(url_for('admin_home'))
                else:
                    flash(f'Welcome !! You are now logged in.','success')
                    return redirect(url_for('customer_home'))
                
            else:
                flash(f'Invalid Credentials', 'success')
                return redirect(url_for('admin_login'))               

        else:
            flash(f'Username does not exist', 'success')
            return redirect(url_for('login'))

    return render_template('user/login.html',title='Login page',form=form)