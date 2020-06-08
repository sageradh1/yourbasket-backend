import secrets
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False

    GENERATED_CUSTOMER_INVOICE_FOLDER= basedir+"/app/static/static/pdf/customer-invoices"

 

    UPLOADED_PHOTOS_DEST = basedir+ '/app/static/images/item-images'
    DEFAULT_PHOTO_FOR_ITEMS = "no-image.png"

    # THUMBNAIL_FOR_UPLOADED_VIDEO_FOLDER = basedir+"/app/static/img/generated/thumbnails"
    
    # MAX_VIDEO_FILESIZE = 100 * 1024 * 1024 #max allowed video filesize is 16MB
    # MAX_CSV_FILESIZE = 10 * 1024 * 1024 #max allowed csv filesize is 10MB

    # BASE_URL_WITH_PORT = "http://127.0.0.1:5000"
    # BASE_URL_WITH_PORT = "http://18.221.137.201"
    # BASE_URL_WITH_PORT = "http://asmi.co"
    
    # ALLOWED_VIDEO_EXTENSIONS = set(['mp4', 'mkv'])
    # ALLOWED_USERDATA_EXTENSIONS = set(['csv'])

    SESSION_COOKIE_SECURE = True

    SECRET_KEY = os.getenv('WEBAPP_SECRET_KEY')
    
class DevelopmentConfig(Config):
    DEBUG = True
    
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_SQLALCHEMY_DATABASE_URI')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DB_NAME = os.getenv('DEV_DB_NAME')
    DB_USERNAME = os.getenv('DEV_DB_USERNAME')
    DB_PASSWORD = os.getenv('DEV_DB_PASSWORD')

    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True

    DB_NAME = os.getenv('TEST_DB_NAME')
    DB_USERNAME = os.getenv('TEST_DB_USERNAME')
    DB_PASSWORD = os.getenv('TEST_DB_PASSWORD')

    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('PRODUCTION_SQLALCHEMY_DATABASE_URI')