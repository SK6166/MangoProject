from bson.objectid import ObjectId

class Book:
    def __init__(self, title, author_id, year, genre="Unknown", available=True, _id=None):
        self._id = _id
        self.title = title
        self.author_id = author_id
        self.year = year
        self.genre = genre
        self.available = available

    def to_dict(self):
        return {
            'title': self.title,
            'author_id': self.author_id,
            'year': self.year,
            'genre': self.genre,
            'available': self.available
        }

    @staticmethod
    def from_dict(data):
        return Book(
            _id=data.get('_id'),
            title=data.get('title'),
            author_id=data.get('author_id'),
            year=data.get('year'),
            genre=data.get('genre', 'Unknown'),
            available=data.get('available', True)
        )