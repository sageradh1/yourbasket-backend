from app import app,db
from app.user.models import User 

user = User(username="yourbasketadmin",urole="admin")
User.set_password(user, "Coronarocks2020")
User.save_to_db(user)