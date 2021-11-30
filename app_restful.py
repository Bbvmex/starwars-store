from itertools import product
from typing import Dict
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from flask_restful import fields, marshal_with
from pymongo import MongoClient
import bcrypt
from common.common import UserExists, EmptyCart, ProductInCart, genReturnJson, ProductExists, verifyPw, verifyCredentials
import json, bson
from resources.user import User
from resources.cart import Cart
from resources.product import Product
from db.db import users, carts, products

app = Flask(__name__)
api = Api(app)

'''
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bson.ObjectId):
            return str(obj)
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return super(MyEncoder, self).default(obj) 

app.json_encoder = MyEncoder'''

api.add_resource(User, '/user/')
api.add_resource(Cart, '/cart/')
api.add_resource(Product, '/product/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug = True)
