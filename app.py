import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError

from resources.confirmation import ConfirmationByUser, Confirmation
from resources.user import UserRegister, UserLogin, UserLogout, TokenRefresh
from resources.product import Product, ProductList
from blacklist import BLACKLIST

from flask_cors import CORS

app = Flask(__name__)

# To solve CORS issues
CORS(app)
cors = CORS(
    app,
    resources={
        r"/*": {
            "origins": "*"
        }
    }
)


app.config["APP"] = "app.py"
app.config["ENV"] = "development"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

app.secret_key = os.environ.get("APP_SECRET_KEY")  # app.config['JWT_SECRET_KEY]

api = Api(app)

# API Endpoints
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/token/refresh')
# Products Endpoints
api.add_resource(ProductList, '/products')
api.add_resource(Product, '/product/<string:name>')
api.add_resource(Confirmation, '/user/confirmation/<string:confirmation_id>')
api.add_resource(ConfirmationByUser, '/user/confirmation/<int:user_id>')


@app.before_first_request
def create_tables():
    """
    Create table at first if not exists
    :return:
    """
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(error):
    """
    Return error wherever the Validation Error occurs.
    This function removes redundant check in every Schema.
    :param error:
    :return error response JSON:
    """
    return jsonify(error.messages), 400


jwt = JWTManager(app)


# This is an example of a complex object that we could
# build a JWT from. In practice, this will likely be
# something like a SQLAlchemy instance
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.username


@jwt.expired_token_loader
def expired_token_callback():
    """
    Send error message if JWT is expired.
    """
    return jsonify({
        'description': 'The token has expired',
        'error': 'token_expired'
    }), 401


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    """
    Send error message if JWT is blacklisted.
    """
    return decrypted_token['jti'] in BLACKLIST


@jwt.invalid_token_loader
def invalid_token_callback(error):
    """
    Send error message if JWT is invalid.
    """
    return jsonify({
        'description': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    """
    Send error message if JWT does not have access token.
    """
    return jsonify({
        'description': 'Request does not contain an access token',
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    """
    Send error message if JWT does not have fresh access token.
    """
    return jsonify({
        'description': 'The token is not fresh',
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    """
    Send error message if JWT is revoked.
    """
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    })


@app.route('/')
def home():
    return 'Your basket API are running '


if __name__ == '__main__':
    from database import db
    from ma import ma
    global db
    db.init_app(app)
    ma.init_app(app)
    # app.run(port=4000, debug=True)
    app.run(host='0.0.0.0',port=4000, debug=True)
