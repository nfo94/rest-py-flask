from flask_restful import Resource, reqparse
from models.user import UserModel


class User(Resource):
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found'}, 404

    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
                return {'message': 'User deleted'}
            except:
                return {'message': 'An error ocurred'}, 500
        return {'message': 'User not found'}, 404


class UserRegister(Resource):
    def post(self):
        arguments = reqparse.RequestParser()
        arguments.add_argument('login', type=str, required=True,
                               help="The field 'login' cannot be left blank")
        arguments.add_argument('password', type=str, required=True,
                               help="The field 'password' cannot be left blank")
        data = arguments.parse_args()
        if UserModel.find_by_login(data['login']):
            return {'message':
                    "The login '{}' user already exists".format(data['login'])}
        user = UserModel(**data)
        user.save_user()
        return {'message': 'User created successfully'}, 201
