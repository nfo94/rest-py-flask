from flask_restful import Resource, reqparse
from models.philosopher import PhilosopherModel


class Philosophers(Resource):
    def get(self):
        return {'philosophers': [philosopher.json() for philosopher in
                                 PhilosopherModel.query.all()]}


class Philosopher(Resource):
    arguments = reqparse.RequestParser()
    arguments.add_argument('name', type=str, required=True,
                           help="Cannot leave this field empty")
    arguments.add_argument('reviews', type=int, required=True,
                           help="Cannot leave this field empty")

    def post(self, id):
        if PhilosopherModel.find_philosopher(id):
            return {'message':
                    'Philosopher id {} already exists.'.format(id)}, 400

        data = Philosopher.arguments.parse_args()
        new_philosopher = PhilosopherModel(id, **data)
        try:
            new_philosopher.save_philosopher()
        except:
            return {'message': 'An error ocurred'}, 500

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
        try:
            philosopher.save_philosopher()
        except:
            return {'message': 'An error ocurred'}, 500

        return philosopher.json(), 201

    def delete(self, id):
        philosopher = PhilosopherModel.find_philosopher(id)
        if philosopher:
            try:
                philosopher.delete_philosopher()
                return {'message': 'Philosopher deleted'}
            except:
                return {'message': 'An error ocurred'}, 500

        return {'message': 'Philosopher not found'}, 404
