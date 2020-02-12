from flask import Flask
from flask_restful import Api
from resources.philosopher import Philosophers, Philosopher
from resources.user import User, UserRegister, UserLogin
from flask_jwt_extended import JWTManager


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///philosoup.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'
api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def create_database():
    database.create_all()


api.add_resource(Philosophers, '/philosophers')
api.add_resource(Philosopher, '/philosophers/<string:id>')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserRegister, '/signup')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    from sql_alchemy import database
    database.init_app(app)
    app.run(debug=True)
