from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_restful import fields, marshal_with

app = Flask(__name__)
api = Api(app)


users = {
    'Teste': {'password': 'pass'}
}

# Add arguments to be used in the functions
parser = reqparse.RequestParser()
parser.add_argument('username', type=str, help='User invalid', required = True)
parser.add_argument('password', type=str, help='Invalid Password')
parser.add_argument('tester', type=int, help='Liar')


def abort_if_user_doesnt_exist(username):
    if username not in users:
        abort(404, message='User doesnt exist')


class User(Resource):
    def get(self):
        args = parser.parse_args()
        username = args['username']
        print(args['tester'])
        abort_if_user_doesnt_exist(username)
        return users[username], 200

    def post(self):
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        users[username] = {'password': password}
        return users, 200

    def delete(self):
        args = parser.parse_args()
        username = args['username']
        del(users[username])
        return users, 200


        
api.add_resource(User, '/user/')

if __name__ == '__main__':
    app.run(debug=True)

