from flask_restful import Resource, reqparse, abort
from flask_restful import fields, marshal_with
import bcrypt
from db.db import users, carts
from common.common import UserExists

cart_args = reqparse.RequestParser()
cart_args.add_argument('username', type=str, required=True, help='Username required')
cart_args.add_argument('password', type=str, required=True, help='Missing password')
cart_args.add_argument('product', type=dict, help='Need to specify one product')
cart_args.add_argument('quantity', type=dict, help='Need to specify the quantity')


class Cart(Resource):
    def get(self):
        args = cart_args.parse_args()
        username = args['username']
        password = args['password']
        if not UserExists(username):
            abort(404, message='User does not exist')
        return carts.find_one({'username': username},
                            {'_id': False,
                            'password': False,
                            'username': False}), 200

    def delete(self):
        args = cart_args.parse_args()
        username = args['username']
        password = args['password']
        if not UserExists(username):
            abort(404,message='User does not exist')
        users.find_one_and_delete({'username': username})
        carts.find_one_and_delete({'username': username})
        return 'User deleted', 204

    def post(self):
        args = cart_args.parse_args()
        username = args['username']
        password = args['password']
        if UserExists(username):
            abort(404, message='User already exists')
        
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

#        if app.debug:
#            return users
        return 'User added', 200