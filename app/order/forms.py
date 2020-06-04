from wtforms import IntegerField,SelectField,validators,StringField
from app.order.models import CustomerOrder,OrderStatus
from flask_wtf import FlaskForm

allorderstatus = OrderStatus.query.all()
# IDS_STATUSES = [(each.id,each.name) for each in allorderstatus]
IDS_STATUSES = [(each.name,each.name) for each in allorderstatus]

class UpdateOrderByStaff(FlaskForm):
    id = IntegerField("ID",default=0)
    invoice_number = StringField('Invoice number: ', [validators.DataRequired()])
    status = StringField('Current Status:', [validators.DataRequired()])
    orderstatus = SelectField('New Status', choices=IDS_STATUSES)