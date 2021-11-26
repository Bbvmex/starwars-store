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
items = db["items"]

def UserExists(username):
    if users.count_documents({"Username": username}) == 0:
        return False
    else:
        return True

def genReturnJson(status, msg):
    returnJson = {
        'status': status,
        'msg': msg
    }
    return returnJson

@app.route('/')
def index():
    return jsonify(genReturnJson(200, 'Index page'))

#@app.route('/user/register', methods=['POST'])
class RegisterUser(Resource):
    def post(self):
        #data = request.get_json()
        data = request.form
        print(data)
        username = data['username']
        print(username)
        password = data['password']

        if UserExists(username):
            return genReturnJson(301, 'Username already exists')
        
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        users.insert({
            'Username': username,
            'Password': hashed_pw,
            'Carrinho': {}
        })

        return jsonify(genReturnJson(200, 'User successfully added'))

api.add_resource(RegisterUser, '/user/register')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
