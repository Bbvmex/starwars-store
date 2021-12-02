from flask_restful import Resource, reqparse, abort
from flask_restful import fields, marshal_with
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required
import datetime

from db.db import users, carts
from common.common import UserExists

user_args = reqparse.RequestParser()
user_args.add_argument('username', type=str, required=True, help='Username required')
user_args.add_argument('password', type=str, required=True)

class User(Resource):
    @jwt_required
    def get(self):
        args = user_args.parse_args()
        username = args['username']
        if not UserExists(username):
            abort(404, message='User does not exist')
        return users.find_one({'username': username},
                            {'_id': False,
                            'password': False}), 200
    @jwt_required
    def delete(self):
        args = user_args.parse_args()
        username = args['username']
        password = args['password']
        if not UserExists(username):
            abort(404,message='User does not exist')
        users.find_one_and_delete({'username': username})
        carts.find_one_and_delete({'username': username})
        return 'User deleted', 204

    def post(self):
        args = user_args.parse_args()
        username = args['username']
        password = args['password']
        if UserExists(username):
            abort(404, message='User already exists')
        
        hashed_pw = generate_password_hash(password)

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

# Generates the access token for the user.
# It will be used as a request argument to access the database
class LogIn(Resource):
    def post(self):
        args = args = user_args.parse_args()
        username = args['username']
        password = args['password']

        if not UserExists(username):
            abort(404, message='User does not exist')
        
        stored_pw = users.find_one({'username': username})['password']
        authorized = check_password_hash(stored_pw, password)
        if not authorized:
            return 'User or password invalid', 401
        
        expires = datetime.timedelta(hours=1)
        access_token = create_access_token(identity=username, expires_delta=expires)
        return {'token': access_token}, 200