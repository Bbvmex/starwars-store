from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import json

from resources.user import User, LogIn
from resources.cart import Cart
from resources.product import Product

app = Flask(__name__)
app.config.from_file('.env', load=json.load)

api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

api.add_resource(User, '/user/')
api.add_resource(LogIn, '/user/login/')
api.add_resource(Cart, '/cart/')
api.add_resource(Product, '/product/')
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug = True)
