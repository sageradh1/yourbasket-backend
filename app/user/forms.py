from wtforms import  StringField,  PasswordField,SubmitField,validators
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    username = StringField('Username: ', [ validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired()])
