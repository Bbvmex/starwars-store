from flask import Flask
from flask_restful import Api
from resources.user import User
from resources.cart import Cart
from resources.product import Product

app = Flask(__name__)
api = Api(app)

api.add_resource(User, '/user/')
api.add_resource(Cart, '/cart/')
api.add_resource(Product, '/product/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug = True)
