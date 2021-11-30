from flask_restful import Resource, reqparse, abort
from flask_restful import fields, marshal_with
from db.db import products
from common.common import ProductExists

prod_args = reqparse.RequestParser()
prod_args.add_argument('id', type=str, required=True, help='Product ID required')
prod_args.add_argument('name', type=str, help='Missing product name')
prod_args.add_argument('quantity', type=int, help='Missing quantity')
prod_args.add_argument('value', type=float, help='Missing value')

class Product(Resource):
    def get(self):
        args = prod_args.parse_args()
        id = args['id']
        return products.find_one({'id': id},
                            {'_id': False,
                            }), 200

    def post(self):
        args = prod_args.parse_args()
        id = args['id']
        name = args['name']
        stock = args['quantity']
        value = args['value']

        if ProductExists(id):
            return 'Product id already exists', 400
        
        products.insert_one(
            {'id': id,
            'name': name,
            'stock': stock,
            'value': value})
        
        return 'New product added', 200

    def delete(self):
        args = prod_args.parse_args()
        id = args['id']

        if not ProductExists(id):
            return 'Product id does not exist', 400
        
        products.find_one_and_delete({'id': id})
        return 'Product removed', 200