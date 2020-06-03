from wtforms import Form, ValidationError,SubmitField,IntegerField,FloatField,StringField,SelectField,TextAreaField,validators
from wtforms.widgets import HiddenInput
from flask_wtf.file import FileField,FileRequired,FileAllowed
from app.product.models import Category,Item
from flask_wtf import FlaskForm

allcategories = Category.query.all()
IDS_CATEGORIES = [(each.id,each.name) for each in allcategories]
# print(IDS_CATEGORIES)


#Custom validator using class
# class ItemNameValidator(object):
#     def __init__(self, message=None):
#         if not message:
#             message = u'Name has been already used !'
#         self.message = message

#     def __call__(self, form, field):
#         if Item.query.filter_by(name=field.data).first():
#             raise ValidationError(self.message)

class Additems(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    price = FloatField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)

    left_quantity = IntegerField('Left Quantity', [validators.DataRequired()])
    quantity_measuring_unit = StringField('Unit measured in ', [validators.DataRequired()])
    desc = TextAreaField('Description', [validators.DataRequired()])

    category_id = SelectField('Category Id', choices=IDS_CATEGORIES,coerce=int)
    
    image_1 = FileField(
        'Main Image',
        validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'],'Images only please')]
    )
    image_2 = FileField('First side image', validators=[ FileAllowed(['jpg','png','gif','jpeg'], 'Images only please')])
    image_3 = FileField('Second side image', validators=[ FileAllowed(['jpg','png','gif','jpeg'], 'Images only please')])

    def validate_name(self, name):
        print("validation running")
        if Item.query.filter_by(name=name.data).first():
            raise ValidationError("This item name is already in use!")

class Updateitems(FlaskForm):
    id = IntegerField("ID",default=0)
    name = StringField('Name', [validators.DataRequired()])
    price = FloatField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)

    left_quantity = IntegerField('Left Quantity', [validators.DataRequired()])
    quantity_measuring_unit = StringField('Unit measured in ', [validators.DataRequired()])
    desc = TextAreaField('Description', [validators.DataRequired()])

    category_id = SelectField('Category Id', choices=IDS_CATEGORIES,coerce=int)
    
    image_1 = FileField(
        'Main Image',
        validators=[FileAllowed(['jpg','png','gif','jpeg'],'Images only please')]
    )
    image_2 = FileField('First side image', validators=[ FileAllowed(['jpg','png','gif','jpeg'], 'Images only please')])
    image_3 = FileField('Second side image', validators=[ FileAllowed(['jpg','png','gif','jpeg'], 'Images only please')])

    def validate_name(self, name):

        if name.data == Item.query.get_or_404(self.id.data).name:
            pass
        else:

            # results = [c for c in Item.query.all() if c.name != name.data]

            # if name.data in [each.name for each in results]:
            #     raise ValidationError("This item name is already in use!")
            print("validation running")
            if Item.query.filter_by(name=name.data).first():
                raise ValidationError("This item name is already in use!")

class Addcategories(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])

    #custom validator using validator_{fieldname}
    def validate_name(self, name):
        if Category.query.filter_by(name=name.data).first():
            raise ValidationError("This category name is already in use!")