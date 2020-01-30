from flask_restful import Resource, reqparse
from models.philosopher import PhilosopherModel

philosophers = [
    {
        'id': '42524634',
        'name': 'Immanuel Kant',
        'reviews': 4.0
    },
    {
        'id': '09807134',
        'name': 'Friedrich Nietzsche',
        'reviews': 4.9
    },
    {
        'id': '12098102',
        'name': 'Jeremy Bentham',
        'reviews': 3.8
    },
]

class Philosophers(Resource):
    def get(self):
        return philosophers

class Philosopher(Resource):
    arguments = reqparse.RequestParser()
    arguments.add_argument('name')
    arguments.add_argument('reviews')

    def find_philosopher(id):
        for philosopher in philosophers:
            if philosopher['id'] == id:
                return philosopher
        return None

    def get(self, id):
        philosopher = Philosopher.find_philosopher(id)

        if philosopher:
            return philosopher
        return {'message': 'Philosopher not found'}, 404

    def post(self, id):
        data = Philosopher.arguments.parse_args()

        new_philosopher_obj = PhilosopherModel(id, **data)
        new_philosopher = new_philosopher_obj.json()

        philosophers.append(new_philosopher)
        return new_philosopher, 200

    def put(self, id):
        data = Philosopher.arguments.parse_args()

        new_philosopher_obj = PhilosopherModel(id, **data)
        new_philosopher = new_philosopher_obj.json()

        philosopher = Philosopher.find_philosopher(id)
        if philosopher:
            philosopher.update(new_philosopher)
            return philosopher, 200

        philosophers.append(new_philosopher)
        return new_philosopher, 201

    def delete(self, id):
        global philosophers
        philosophers = [philosopher for philosopher in philosophers if philosopher['id'] != id]
        return {'message': 'Philosopher deleted'}
