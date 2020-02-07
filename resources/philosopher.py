from flask_restful import Resource, reqparse
from models.philosopher import PhilosopherModel


class Philosophers(Resource):
    def get(self):
        return {'philosophers': [philosopher.json() for philosopher in PhilosopherModel.query.all()]}


class Philosopher(Resource):
    arguments = reqparse.RequestParser()
    arguments.add_argument('name')
    arguments.add_argument('reviews')

    def post(self, id):
        if PhilosopherModel.find_philosopher(id):
            return {'message': 'Philosopher id {} already exists.'.format(id)}, 400

        data = Philosopher.arguments.parse_args()
        new_philosopher = PhilosopherModel(id, **data)
        new_philosopher.save_philosopher()

        return new_philosopher.json()

    def get(self, id):
        philosopher = PhilosopherModel.find_philosopher(id)

        if philosopher:
            return philosopher.json()

        return {'message': 'Philosopher not found'}, 404

    def put(self, id):
        data = Philosopher.arguments.parse_args()

        found_philosopher = PhilosopherModel.find_philosopher(id)
        if found_philosopher:
            found_philosopher.update_philosopher(**data)
            found_philosopher.save_philosopher()
            return found_philosopher.json(), 200

        philosopher = PhilosopherModel(id, **data)
        philosopher.save_philosopher()

        return philosopher.json(), 201

    def delete(self, id):
        philosopher = PhilosopherModel.find_philosopher(id)
        if philosopher:
            philosopher.delete_philosopher()
            return {'message': 'Philosopher deleted'}

        return {'message': 'Philosopher not found'}, 404
