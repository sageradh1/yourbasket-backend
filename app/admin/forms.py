from wtforms import StringField, PasswordField, validators 
from flask_wtf import FlaskForm

class AdminLoginForm(FlaskForm):
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [validators.DataRequired()])