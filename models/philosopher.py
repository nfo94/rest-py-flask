from sql_alchemy import database


class PhilosopherModel(database.Model):
    __tablename__ = 'philosophers'

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(50))
    reviews = database.Column(database.Float(precision=2))

    def __init__(self, id, name, reviews):
        self.id = id
        self.name = name
        self.reviews = reviews

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'reviews': self.reviews
        }

    @classmethod
    def find_philosopher(cls, id):
        philosopher = cls.query.filter_by(id=id).first()
        if philosopher:
            return philosopher
        return None

    def save_philosopher(self):
        database.session.add(self)
        database.session.commit()

    def update_philosopher(self, name, reviews):
        self.name = name
        self.reviews = reviews

    def delete_philosopher(self):
        database.session.delete(self)
        database.session.commit()
