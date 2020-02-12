from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import safe_str_cmp

arguments = reqparse.RequestParser()
arguments.add_argument('login', type=str, required=True,
                       help="The field 'login' cannot be left blank")
arguments.add_argument('password', type=str, required=True,
                       help="The field 'password' cannot be left blank")


class User(Resource):
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found'}, 404

    @jwt_required
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
        data = arguments.parse_args()
        if UserModel.find_by_login(data['login']):
            return {'message':
                    "The login '{}' user already exists".format(data['login'])}
        user = UserModel(**data)
        user.save_user()
        return {'message': 'User created successfully'}, 201


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = arguments.parse_args()
        user = UserModel.find_by_login(data['login'])
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.user_id)
            return {'access_token': access_token}, 200
        return {'message': 'The username or password is incorrect'}, 401
