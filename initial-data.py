from app import app,db


from app.user.models import User 
user = User(username="yourbasketadmin",urole="admin")
User.set_password(user, "Coronarocks2020")
User.save_to_db(user)


from app.order.models import OrderStatus
orderstatuslist=["Ordered","Packaged","Delivering","Delivered","Cancelled","Updated"]
for eachstatus in orderstatuslist:
    db.session.add((OrderStatus(name=eachstatus)))
db.session.commit()