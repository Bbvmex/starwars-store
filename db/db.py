from pymongo import MongoClient
import certifi

connection_string = "mongodb+srv://teste:teste_dev@hugovm-dev.vta9r.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = MongoClient(connection_string, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=5000)
db = client.starwars_shop
users = db["users"]
products = db["products"]
carts = db['carts']
