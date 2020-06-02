from wtforms import Form, StringField, TextAreaField, PasswordField,SubmitField,validators, ValidationError,DateField
from flask_wtf.file import FileRequired,FileAllowed, FileField
from flask_wtf import FlaskForm
from app.user.models import User

class CustomerRegisterForm(FlaskForm):
    first_name = StringField('First Name: ')
    last_name = StringField('Last Name: ')

    username = StringField('Username: ', [validators.DataRequired()])

    email = StringField('Email: ', [validators.Email(), validators.Optional()])
    password = PasswordField('Password: ', [validators.DataRequired(), validators.EqualTo('confirm', message=' Both password must match! ')])
    confirm = PasswordField('Confirm Password: ', [validators.DataRequired()])
    
    city = StringField('City: ', [validators.DataRequired()])
    address = StringField('Address: ', [validators.DataRequired()])

    contactnumber = StringField('Contact Number: ', [validators.DataRequired()])

    dob= DateField('DOB',[validators.Optional()],format='%Y-%m-%d')
    # profile = FileField('Profile', validators=[FileAllowed(['jpg','png','jpeg','gif'], 'Image only please')])
    
    submit = SubmitField('Register')

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("This username is already in use!")
        
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("This email address is already in use!")
