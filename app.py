from itertools import product
from typing import Dict
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb+srv://teste:teste_dev@hugovm-dev.vta9r.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# db = client.test
db = client.starwars_shop
users = db["users"]
products = db["products"]
carts = db['carts']

def UserExists(username):
    if users.count_documents({"username": username}) == 0:
        return False
    else:
        return True

def EmptyCart(username):
    if carts.find_one({'username': username})['products'] == {}:
        return True
    else:
        return False

def ProductInCart(username, id):
    if carts.find_one({'username': username})['products'].get(id) is None:
        return False
    else:
        return True

def genReturnJson(status, msg):
    returnJson = {
        'status': status,
        'msg': msg
    }
    return returnJson

def ProductExists(id):
    if products.count_documents({'id': id}) == 0:
        return False
    else:
        return True

def verifyPw(username, password):
    if not UserExists(username):
        return False

    hashed_pw = users.find({
        "username":username
    })[0]["password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False

def verifyCredentials(username, password):
    if not UserExists(username):
        return genReturnJson(301, "Invalid Username"), True

    correct_pw = verifyPw(username, password)

    if not correct_pw:
        return genReturnJson(302, "Incorrect Password"), True

    return None, False

@app.route('/')
def index():
    return jsonify(genReturnJson(200, 'Index page'))

#@app.route('/user/register', methods=['POST'])
class RegisterUser(Resource):
    def post(self):
        data = request.form
        username = data['username']
        password = data['password']

        if UserExists(username):
            return genReturnJson(301, 'Username already exists')
        
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        users.insert_one({
            'username': username,
            'password': hashed_pw,
            'cart': {}
        })
        carts.insert_one({
            'username': username,
            'products': {}
        })

        return jsonify(genReturnJson(200, 'User successfully added'))

class DeleteUser(Resource):
    def post(self):
        data = request.form
        username = data['username']

        if not UserExists(username):
            return genReturnJson(302, 'Username does not exist')
        
        users.delete_one({'username': username})
        carts.delete_one({'username': username})

        return jsonify(genReturnJson(200, 'User successfuly deleted'))

class AddToCart(Resource):
    def post(self):
        data = request.form
        username = data['username']
        password = data['password']
        product_id = data['id']
        quantity = int(data['quantity'])

        # Check if user exists
        returnJson, error = verifyCredentials(username, password)
        if error:
            return jsonify(returnJson)
        
        if not ProductExists(product_id):
            return jsonify(genReturnJson(303, 'Product id does not exist'))
        
        carts.find_one_and_update(
            {'username': username},
            {'$inc': {'products.'+product_id: quantity}},
            upsert = True)
        
        return jsonify(genReturnJson(200, 'Product added to cart'))

class RemoveFromCart(Resource):
    def post(self):
        data = request.form
        username = data['username']
        password = data['password']
        product_id = data['id']
        quantity = int(data['quantity'])

        # Check if user exists
        returnJson, error = verifyCredentials(username, password)
        if error:
            return jsonify(returnJson)
        
        if not ProductExists(product_id):
            return jsonify(genReturnJson(303, 'Product id does not exist'))
        
        if not ProductInCart(username, product_id):
            return jsonify(genReturnJson(304, 'Product not in cart'))

        carts.find_one_and_update(
            {'username': username},
            {'$inc': {'products.'+product_id: -quantity}},
            upsert = False)

        if carts.find_one({'username': username})['products'][product_id] < 0:
            carts.find_one_and_update(
                {'username': username},
                {'$unset': {'products.'+product_id: ""}},
                upsert = False)
        
        return jsonify(genReturnJson(200, 'Product removed from cart'))

class AddNewProduct(Resource):
    def post(self):
        data = request.form
        product_id = data['id']
        name = data['name']
        stock = int(data['quantity'])
        value = float(data['value'])

        if ProductExists(product_id):
            return jsonify(genReturnJson(303, 'Product id already exists'))
        
        products.insert_one(
            {'id': product_id,
            'name': name,
            'stock': stock,
            'value': value})
        
        return jsonify(genReturnJson(200, 'New product added'))

class RemoveProduct(Resource):
    def post(self):
        data = request.form
        product_id = data['id']

        if not ProductExists(product_id):
            return jsonify(genReturnJson(305, 'Product id does not exist'))
        
        products.find_one_and_delete({'id': product_id})
        
        return jsonify(genReturnJson(200, 'Product removed'))





api.add_resource(RegisterUser, '/user/register')
api.add_resource(DeleteUser, '/user/delete')
api.add_resource(AddToCart, '/cart/add')
api.add_resource(RemoveFromCart, '/cart/remove')
api.add_resource(AddNewProduct, '/products/new')
api.add_resource(RemoveProduct, '/products/remove')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
