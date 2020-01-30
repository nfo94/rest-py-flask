from flask import Flask
from flask_restful import Api
from resources.philosopher import Philosophers, Philosopher

app = Flask(__name__)
api = Api(app)

api.add_resource(Philosophers, '/philosophers')
api.add_resource(Philosopher, '/philosophers/<string:id>')


if __name__ == '__main__':
    app.run(debug=True)
