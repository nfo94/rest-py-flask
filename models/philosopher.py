class PhilosopherModel:
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
