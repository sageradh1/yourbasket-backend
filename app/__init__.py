from flask import Flask,session,g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import timedelta
import os
from dotenv import load_dotenv
from flask_login import LoginManager,current_user
from functools import wraps
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
# from werkzeug.utils import secure_filename
from flask_msearch import Search
app = Flask(__name__)

#To change default locations
# app = Flask(__name__,
#             static_url_path='', 
#             static_folder='web/static',
#             template_folder='web/templates')


#Loading environment from .startingenv
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

app.config["APP"] = os.getenv('FLASK_APP')
app.config["ENV"] = os.getenv('FLASK_ENV')
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=7)

#Loading which configuration to use
if app.config["ENV"]=="development":
    app.config.from_object("config.DevelopmentConfig")
elif app.config["ENV"]=="testing":
    app.config.from_object("config.TestingConfig")
else:
    app.config.from_object("config.ProductionConfig")

print("The environment is : "+app.config["ENV"])
print(f"The current database being used is : ${app.config['DB_NAME']} ")

#Global variables for categories and products
# session['globalcategories'] = []
# session['globalproducts']=[]

#Loading db instance
db = SQLAlchemy(app)

#Migration of database
migrate = Migrate(app, db)
with app.app_context():
    if db.engine.url.drivername == "sqlite":
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)


#Loading login manager 
login = LoginManager(app)
login.login_view = 'login'
login.needs_refresh_message_category='danger'
login.login_message = u"Please login with approriate id first"

#Adding role usage in flask login using custom decorator
def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
              return login.unauthorized()
            if ((current_user.urole != role) and (role != "ANY")):
                return login.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

# Setting timeout for session cookie (It is not a setting for remember_token cookie set by flask_login)
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = app.config["REMEMBER_COOKIE_DURATION"]

#Upload photo functionality
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

# Search functionality
search = Search()
search.init_app(app)

#Loading database models
from app.user import models #also has load_user for Loginmanager 
from app.product import models
from app.order import models

#Loading routes/views
from app.user import routes
from app.customer import routes
from app.product import routes
from app.cart import carts
from app.order import orders
from app.admin import routes
from app.staff import routes


# # Admin Dashboard feature
# from flask_admin.contrib.sqla import ModelView
# from flask_admin import Admin
# from app.product.models import Category,Item
# admin = Admin(app)
# admin.add_view(ModelView(Category,db.session))
# admin.add_view(ModelView(Item,db.session))