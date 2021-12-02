from flask_restful import Resource, reqparse, abort
from flask_restful import fields, marshal_with
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_httpauth import HTTPBasicAuth
import datetime

from db.db import users, carts
from common.common import UserExists

auth = HTTPBasicAuth()

user_args = reqparse.RequestParser()
user_args.add_argument('username', type=str, required=True, help='Username required')
user_args.add_argument('password', type=str, required=True)

@auth.verify_password
def verify_password(username, password):
    user = users.find_one({'username': username})
    stored_pw = user['password']
    authorized = check_password_hash(stored_pw, password)
    if not user or not authorized:
        return False
    #g.user = user
    return True

class User(Resource):
    def get(self):
        decorators = [jwt_required]
        args = user_args.parse_args()
        username = args['username']
        password = args['password']
        if not UserExists(username):
            abort(404, message='User does not exist')
        return users.find_one({'username': username},
                            {'_id': False,
                            'password': False}), 200

    #@jwt_required
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