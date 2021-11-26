from pymongo import MongoClient

# client = MongoClient("mongodb://db:27017")
client = MongoClient("mongodb+srv://teste:teste_dev@hugovm-dev.vta9r.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# db = client.test
db = client.starwars_shop
users = db["users"]
items = db["items"]

# A string de conexão será hard-coded para teste
class db_instance:
    def __init__(self) -> None:
        client = MongoClient("mongodb+srv://teste:teste_dev@hugovm-dev.vta9r.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.db = client.starwars_shop
        self.users = self.db['users']
        self.items = self.db['items']
