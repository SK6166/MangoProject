from pymongo.errors import OperationFailure, PyMongoError

class ReportService:
    def __init__(self, db):
        self.db = db

    def books_by_genre(self):
        try:
            pipeline = [
                {
                    '$group': {
                        '_id': '$genre',
                        'total_books': {'$sum': 1},
                        'avg_year': {'$avg': '$year'},
                        'oldest_book': {'$min': '$year'},
                        'newest_book': {'$max': '$year'}
                    }
                },
                {'$sort': {'total_books': -1}}
            ]
            return list(self.db.books.aggregate(pipeline))
        except OperationFailure as e:
            raise OperationFailure(f"Ошибка БД: {e}")

    def books_by_year(self, year_from, year_to, genre, available):
        query = {}
        search_params = {}

        if year_from:
            query['year'] = query.get('year', {})
            query['year']['$gte'] = int(year_from)
            search_params['year_from'] = year_from

        if year_to:
            query['year'] = query.get('year', {})
            query['year']['$lte'] = int(year_to)
            search_params['year_to'] = year_to

        if genre:
            query['genre'] = genre
            search_params['genre'] = genre

        if available:
            query['available'] = True if available == 'yes' else False
            search_params['available'] = available

        results = list(self.db.books.find(query).sort('year', 1)) if query else []

        summary = {}
        if query:
            pipeline = [
                {'$match': query},
                {
                    '$group': {
                        '_id': '$author_id',
                        'count': {'$sum': 1},
                        'avg_year': {'$avg': '$year'},
                        'titles': {'$push': '$title'}
                    }
                },
                {
                    '$lookup': {
                        'from': 'authors',
                        'localField': '_id',
                        'foreignField': '_id',
                        'as': 'author'
                    }
                },
                {'$unwind': '$author'},
                {'$sort': {'count': -1}}
            ]
            summary_data = list(self.db.books.aggregate(pipeline))

            summary = {
                'total_books': len(results),
                'by_author': summary_data,
                'avg_year_all': sum(b['year'] for b in results) / len(results) if results else 0
            }

        all_genres = self.db.books.distinct('genre')

        return results, summary, search_params, all_genres

    def books_availability(self):
        try:
            pipeline = [
                {
                    '$group': {
                        '_id': '$available',
                        'count': {'$sum': 1}
                    }
                }
            ]
            availability_data = list(self.db.books.aggregate(pipeline))

            available_count = 0
            unavailable_count = 0

            for item in availability_data:
                if item['_id'] == True:
                    available_count = item['count']
                else:
                    unavailable_count = item['count']

            total = available_count + unavailable_count

            pipeline_genres = [
                {
                    '$group': {
                        '_id': {'genre': '$genre', 'available': '$available'},
                        'count': {'$sum': 1}
                    }
                },
                {'$sort': {'_id.genre': 1}}
            ]
            genre_availability = list(self.db.books.aggregate(pipeline_genres))

            return available_count, unavailable_count, total, genre_availability
        except OperationFailure as e:
            raise OperationFailure(f"Ошибка БД: {e}")

    def authors_activity(self):
        try:
            pipeline = [
                {
                    '$group': {
                        '_id': '$author_id',
                        'book_count': {'$sum': 1},
                        'latest_book': {'$max': '$year'},
                        'first_book': {'$min': '$year'},
                        'genres': {'$addToSet': '$genre'}
                    }
                },
                {
                    '$lookup': {
                        'from': 'authors',
                        'localField': '_id',
                        'foreignField': '_id',
                        'as': 'author_info'
                    }
                },
                {'$unwind': '$author_info'},
                {'$sort': {'book_count': -1}}
            ]
            return list(self.db.books.aggregate(pipeline))
        except OperationFailure as e:
            raise OperationFailure(f"Ошибка БД: {e}")

    def authors_by_country(self):
        try:
            pipeline = [
                {
                    '$group': {
                        '_id': '$country',
                        'author_count': {'$sum': 1},
                        'authors': {'$push': '$name'}
                    }
                },
                {'$sort': {'author_count': -1}}
            ]
            return list(self.db.authors.aggregate(pipeline))
        except OperationFailure as e:
            raise OperationFailure(f"Ошибка БД: {e}")

    def authors_by_era(self, birth_from, birth_to, country):
        query = {}
        search_params = {}

        if birth_from:
            query['birth_year'] = query.get('birth_year', {})
            query['birth_year']['$gte'] = int(birth_from)
            search_params['birth_from'] = birth_from

        if birth_to:
            query['birth_year'] = query.get('birth_year', {})
            query['birth_year']['$lte'] = int(birth_to)
            search_params['birth_to'] = birth_to

        if country:
            query['country'] = country
            search_params['country'] = country

        results = list(self.db.authors.find(query).sort('birth_year', 1)) if query else []

        summary = {}
        if query:
            pipeline = [
                {'$match': query},
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
                        'book_count': {'$size': '$books'},
                        'years_active': {
                            '$cond': {
                                'if': {'$gt': [{'$size': '$books'}, 0]},
                                'then': {
                                    'from': {'$min': '$books.year'},
                                    'to': {'$max': '$books.year'}
                                },
                                'else': None
                            }
                        }
                    }
                },
                {'$sort': {'birth_year': 1}}
            ]
            summary_data = list(self.db.authors.aggregate(pipeline))

            summary = {
                'total_authors': len(results),
                'authors_detail': summary_data
            }

        all_countries = self.db.authors.distinct('country')

        return results, summary, search_params, all_countries