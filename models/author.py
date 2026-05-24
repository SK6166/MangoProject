from bson.objectid import ObjectId

class Author:
    def __init__(self, name, country="Unknown", birth_year=None, _id=None):
        self._id = _id
        self.name = name
        self.country = country
        self.birth_year = birth_year

    def to_dict(self):
        data = {
            'name': self.name,
            'country': self.country
        }
        if self.birth_year:
            data['birth_year'] = self.birth_year
        return data

    @staticmethod
    def from_dict(data):
        return Author(
            _id=data.get('_id'),
            name=data.get('name'),
            country=data.get('country', 'Unknown'),
            birth_year=data.get('birth_year')
        )