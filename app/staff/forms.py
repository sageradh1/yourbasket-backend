from wtforms import Form,IntegerField, StringField, TextAreaField, PasswordField,SubmitField,validators, ValidationError,DateField
from flask_wtf.file import FileRequired,FileAllowed, FileField
from flask_wtf import FlaskForm
from app.user.models import User

class StaffRegisterForm(FlaskForm):
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
    
    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("This username is already in use!")
        
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("This email address is already in use!")



class StaffUpdateForm(FlaskForm):
    id = IntegerField("ID",default=0)
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
    

    def validate_username(self, username):
        print("username validation running") 
        if username.data == User.query.get_or_404(self.id.data).username:
            pass
        else:
            if User.query.filter_by(username=username.data).first():
                raise ValidationError("This username is already in use!")
    
    def validate_email(self, email):
        print("email validation running") 
        if email.data == User.query.get_or_404(self.id.data).email:
            pass
        else:
            if User.query.filter_by(email=email.data).first():
                raise ValidationError("This email is already in use!")