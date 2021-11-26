from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
from typing import Dict


app = Flask(__name__)
api = Api(app)

# client = MongoClient("mongodb://db:27017")
client = MongoClient("mongodb+srv://teste:teste_dev@hugovm-dev.vta9r.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# db = client.test
db = client.starwars_shop
users = db["users"]
items = db["items"]



def UserExist(username):
    if users.find({"Username": username}).count == 0:
        return False
    else:
        return True

def ItemExists(id):
    if items.find({"ID": id}).count == 0:
        return False
    else:
        return True

class Register(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]

        if UserExist(username):
            retJson = {
                "status": "301",
                "msg": "Invalid username"
            }
            return jsonify(retJson)

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Carrinho": [],
        })

        retJson = {
            "status": 200,
            "msg": "User inserted successfully"
        }
        return jsonify(retJson)
    
def generateReturnDictionary(status, msg):
    retJson = {
        "status": status,
        "msg": msg
    }
    return retJson

def verifyPw(username, password):
    if not UserExist(username):
        return False
    
    hashed_pw = users.find({
        "Username":username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf-8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False

#ErrorDictionary, True/False
def verifyCredentials(username, password):
    if not UserExist(username):
        return generateReturnDictionary(301, "Invalid Username"), True
    correct_pw = verifyPw(username, password)

    if not correct_pw:
        return generateReturnDictionary(302, "Incorrect Password"), True
    
    return None, False

def verifyItem(id):
    pass


class Add_Cart(Resource):
    def post(self):
        postedData = request.get_json()

        item_id = postedData["id"]
        quantidade = postedData["quantidade"]

    
if __name__ == "__main__":
    app.run(host='0.0.0.0')

