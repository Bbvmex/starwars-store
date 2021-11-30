from pymongo import MongoClient
import bcrypt


client = MongoClient("mongodb+srv://teste:teste_dev@hugovm-dev.vta9r.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.test
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