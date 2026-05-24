from bson.objectid import ObjectId
from pymongo.errors import OperationFailure, PyMongoError

class AuthorService:
    def __init__(self, db):
        self.db = db

    def get_all_with_book_count(self):
        try:
            return list(self.db.authors.aggregate([
                {
                    '$lookup': {
                        'from': 'books',
                        'localField': '_id',
                        'foreignField': 'author_id',
                        'as': 'books'
                    }
                },
                {
                    '$addFields': {
                        'book_count': {'$size': '$books'}
                    }
                },
                {
                    '$project': {
                        'books': 0
                    }
                }
            ]))
        except OperationFailure as e:
            raise OperationFailure(f"Ошибка БД при чтении авторов: {e}")
        except PyMongoError as e:
            raise PyMongoError(f"Ошибка БД: {e}")

    def add(self, name, country, birth_year):
        try:
            author_data = {
                'name': name,
                'country': country or 'Unknown'
            }
            if birth_year:
                author_data['birth_year'] = int(birth_year)
            self.db.authors.insert_one(author_data)
        except OperationFailure as e:
            raise OperationFailure(f"Ошибка БД при добавлении автора: {e}")
        except PyMongoError as e:
            raise PyMongoError(f"Ошибка БД: {e}")

    def update(self, author_id, name, country, birth_year):
        try:
            update_data = {
                'name': name,
                'country': country or 'Unknown'
            }
            if birth_year:
                update_data['birth_year'] = int(birth_year)
            self.db.authors.update_one(
                {'_id': ObjectId(author_id)},
                {'$set': update_data}
            )
        except OperationFailure as e:
            raise OperationFailure(f"Ошибка БД при обновлении автора: {e}")
        except PyMongoError as e:
            raise PyMongoError(f"Ошибка БД: {e}")

    def delete(self, author_id):
        try:
            self.db.books.delete_many({'author_id': ObjectId(author_id)})
            self.db.authors.delete_one({'_id': ObjectId(author_id)})
        except OperationFailure as e:
            raise OperationFailure(f"Ошибка БД при удалении автора: {e}")
        except PyMongoError as e:
            raise PyMongoError(f"Ошибка БД: {e}")