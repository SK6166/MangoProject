from bson.objectid import ObjectId
from pymongo.errors import OperationFailure, PyMongoError

class BookService:
    def __init__(self, db):
        self.db = db

    def get_all_with_authors(self):
        try:
            return list(self.db.books.aggregate([
                {
                    '$lookup': {
                        'from': 'authors',
                        'localField': 'author_id',
                        'foreignField': '_id',
                        'as': 'author'
                    }
                },
                {'$unwind': {'path': '$author', 'preserveNullAndEmptyArrays': True}}
            ]))
        except OperationFailure as e:
            raise OperationFailure(f"Ошибка БД при чтении книг: {e}")
        except PyMongoError as e:
            raise PyMongoError(f"Ошибка БД: {e}")

    def get_all_authors(self):
        try:
            return list(self.db.authors.find())
        except OperationFailure as e:
            raise OperationFailure(f"Ошибка БД при чтении авторов: {e}")

    def add(self, title, year, author_id, genre, available):
        try:
            self.db.books.insert_one({
                'title': title,
                'author_id': ObjectId(author_id),
                'year': int(year),
                'genre': genre or 'Unknown',
                'available': available
            })
        except OperationFailure as e:
            raise OperationFailure(f"Ошибка БД при добавлении книги: {e}")
        except PyMongoError as e:
            raise PyMongoError(f"Ошибка БД: {e}")

    def update(self, book_id, title, year, genre, available):
        try:
            self.db.books.update_one(
                {'_id': ObjectId(book_id)},
                {'$set': {
                    'title': title,
                    'year': int(year),
                    'genre': genre or 'Unknown',
                    'available': available
                }}
            )
        except OperationFailure as e:
            raise OperationFailure(f"Ошибка БД при обновлении книги: {e}")
        except PyMongoError as e:
            raise PyMongoError(f"Ошибка БД: {e}")

    def delete(self, book_id):
        try:
            self.db.books.delete_one({'_id': ObjectId(book_id)})
        except OperationFailure as e:
            raise OperationFailure(f"Ошибка БД при удалении книги: {e}")
        except PyMongoError as e:
            raise PyMongoError(f"Ошибка БД: {e}")

    def search(self, search_term, search_field, year_from):
        query = {}
        search_type = 'simple'

        if search_term:
            if search_field == 'title':
                query['title'] = {'$regex': search_term, '$options': 'i'}
                search_type = 'regex'
            elif search_field == 'text':
                query['$text'] = {'$search': search_term}
                search_type = 'text'
            elif search_field == 'author':
                authors_found = list(self.db.authors.find(
                    {'name': {'$regex': search_term, '$options': 'i'}}
                ))
                author_ids = [a['_id'] for a in authors_found]
                if author_ids:
                    query['author_id'] = {'$in': author_ids}
                else:
                    query['_id'] = None
                search_type = 'author_search'

        if year_from:
            query['year'] = {'$gte': int(year_from)}

        results = list(self.db.books.find(query)) if query else []

        for book in results:
            author = self.db.authors.find_one({'_id': book.get('author_id')})
            book['author_name'] = author['name'] if author else 'Unknown'

        return results, search_type