from pymongo import MongoClient

client = MongoClient("mongodb+srv://teste:teste_dev@hugovm-dev.vta9r.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.starwars_shop
users = db["users"]
products = db["products"]
carts = db['carts']