from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

MONGO_URI = "mongodb://admin_user:admin123@localhost:27017/library_db?authSource=library_db"
client = MongoClient(MONGO_URI)
db = client['library_db']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books')
def books_list():
    books = list(db.books.aggregate([
        {
            '$lookup': {
                'from': 'authors',
                'localField': 'author_id',
                'foreignField': '_id',
                'as': 'author'
            }
        },
        { '$unwind': { 'path': '$author', 'preserveNullAndEmptyArrays': True } }
    ]))
    
    authors = list(db.authors.find())
    
    return render_template('books.html', books=books, authors=authors)

@app.route('/books/add', methods=['POST'])
def add_book():
    title = request.form['title']
    year = int(request.form['year'])
    author_id = ObjectId(request.form['author_id'])
    
    db.books.insert_one({
        'title': title,
        'author_id': author_id,
        'year': year,
        'genre': request.form.get('genre', 'Unknown'),
        'available': 'available' in request.form
    })
    return redirect(url_for('books_list'))

@app.route('/books/update/<string:book_id>', methods=['POST'])
def update_book(book_id):
    db.books.update_one(
        {'_id': ObjectId(book_id)},
        {'$set': {
            'title': request.form['title'],
            'year': int(request.form['year']),
            'genre': request.form.get('genre', 'Unknown'),
            'available': 'available' in request.form
        }}
    )
    return redirect(url_for('books_list'))

@app.route('/books/delete/<string:book_id>')
def delete_book(book_id):
    db.books.delete_one({'_id': ObjectId(book_id)})
    return redirect(url_for('books_list'))

@app.route('/authors')
def authors_list():
    authors = list(db.authors.aggregate([
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
                'book_count': { '$size': '$books' }
            }
        },
        {
            '$project': {
                'books': 0
            }
        }
    ]))
    
    return render_template('authors.html', authors=authors)

@app.route('/authors/add', methods=['POST'])
def add_author():
    name = request.form['name']
    country = request.form.get('country', 'Unknown')
    birth_year = request.form.get('birth_year')
    
    author_data = {
        'name': name,
        'country': country
    }
    
    if birth_year:
        author_data['birth_year'] = int(birth_year)
    
    db.authors.insert_one(author_data)
    return redirect(url_for('authors_list'))

@app.route('/authors/update/<string:author_id>', methods=['POST'])
def update_author(author_id):
    update_data = {
        'name': request.form['name'],
        'country': request.form.get('country', 'Unknown')
    }
    
    birth_year = request.form.get('birth_year')
    if birth_year:
        update_data['birth_year'] = int(birth_year)
    
    db.authors.update_one(
        {'_id': ObjectId(author_id)},
        {'$set': update_data}
    )
    return redirect(url_for('authors_list'))

@app.route('/authors/delete/<string:author_id>')
def delete_author(author_id):
    db.books.delete_many({'author_id': ObjectId(author_id)})
    db.authors.delete_one({'_id': ObjectId(author_id)})
    return redirect(url_for('authors_list'))

@app.route('/report/books_by_genre')
def report_books_by_genre():
    pipeline = [
        {
            '$group': {
                '_id': '$genre',
                'total_books': { '$sum': 1 },
                'avg_year': { '$avg': '$year' },
                'oldest_book': { '$min': '$year' },
                'newest_book': { '$max': '$year' }
            }
        },
        { '$sort': { 'total_books': -1 } }
    ]
    data = list(db.books.aggregate(pipeline))
    return render_template('report_books_by_genre.html', data=data)

@app.route('/report/books_by_year', methods=['GET', 'POST'])
def report_books_by_year():
    results = []
    summary = {}
    search_params = {}
    
    if request.method == 'POST':
        query = {}
        
        year_from = request.form.get('year_from')
        year_to = request.form.get('year_to')
        genre = request.form.get('genre')
        available = request.form.get('available')
        
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
        
        if query:
            results = list(db.books.find(query).sort('year', 1))
        
        if query:
            pipeline = [
                { '$match': query },
                {
                    '$group': {
                        '_id': '$author_id',
                        'count': { '$sum': 1 },
                        'avg_year': { '$avg': '$year' },
                        'titles': { '$push': '$title' }
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
                { '$unwind': '$author' },
                { '$sort': { 'count': -1 } }
            ]
            summary_data = list(db.books.aggregate(pipeline))
            
            summary = {
                'total_books': len(results),
                'by_author': summary_data,
                'avg_year_all': sum(b['year'] for b in results) / len(results) if results else 0
            }
    
    all_genres = db.books.distinct('genre')
    
    return render_template('report_books_by_year.html', 
                         results=results, 
                         summary=summary, 
                         search_params=search_params,
                         all_genres=all_genres)

@app.route('/report/books_availability')
def report_books_availability():
    pipeline = [
        {
            '$group': {
                '_id': '$available',
                'count': { '$sum': 1 }
            }
        }
    ]
    availability_data = list(db.books.aggregate(pipeline))
    
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
                'count': { '$sum': 1 }
            }
        },
        { '$sort': { '_id.genre': 1 } }
    ]
    genre_availability = list(db.books.aggregate(pipeline_genres))
    
    return render_template('report_books_availability.html',
                         available_count=available_count,
                         unavailable_count=unavailable_count,
                         total=total,
                         genre_availability=genre_availability)

@app.route('/report/authors_activity')
def report_authors_activity():
    pipeline = [
        {
            '$group': {
                '_id': '$author_id',
                'book_count': { '$sum': 1 },
                'latest_book': { '$max': '$year' },
                'first_book': { '$min': '$year' },
                'genres': { '$addToSet': '$genre' }
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
        { '$unwind': '$author_info' },
        { '$sort': { 'book_count': -1 } }
    ]
    data = list(db.books.aggregate(pipeline))
    return render_template('report_authors_activity.html', data=data)

@app.route('/report/authors_by_country')
def report_authors_by_country():
    pipeline = [
        {
            '$group': {
                '_id': '$country',
                'author_count': { '$sum': 1 },
                'authors': { '$push': '$name' }
            }
        },
        { '$sort': { 'author_count': -1 } }
    ]
    data = list(db.authors.aggregate(pipeline))
    return render_template('report_authors_by_country.html', data=data)

@app.route('/report/authors_by_era', methods=['GET', 'POST'])
def report_authors_by_era():
    results = []
    summary = {}
    search_params = {}
    
    if request.method == 'POST':
        query = {}
        
        birth_from = request.form.get('birth_from')
        birth_to = request.form.get('birth_to')
        country = request.form.get('country')
        
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
        
        if query:
            results = list(db.authors.find(query).sort('birth_year', 1))
        
        if query:
            pipeline = [
                { '$match': query },
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
                        'book_count': { '$size': '$books' },
                        'years_active': {
                            '$cond': {
                                'if': { '$gt': [{ '$size': '$books' }, 0] },
                                'then': {
                                    'from': { '$min': '$books.year' },
                                    'to': { '$max': '$books.year' }
                                },
                                'else': None
                            }
                        }
                    }
                },
                { '$sort': { 'birth_year': 1 } }
            ]
            summary_data = list(db.authors.aggregate(pipeline))
            
            summary = {
                'total_authors': len(results),
                'authors_detail': summary_data
            }
    
    all_countries = db.authors.distinct('country')
    
    return render_template('report_authors_by_era.html',
                         results=results,
                         summary=summary,
                         search_params=search_params,
                         all_countries=all_countries)

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    query = {}
    search_type = 'simple'
    
    if request.method == 'POST':
        search_term = request.form.get('search')
        search_field = request.form.get('search_field', 'title')
        year_from = request.form.get('year_from')
        
        if search_term:
            if search_field == 'title':
                query['title'] = {'$regex': search_term, '$options': 'i'}
                search_type = 'regex'
            elif search_field == 'text':
                query['$text'] = {'$search': search_term}
                search_type = 'text'
            elif search_field == 'author':
                authors_found = list(db.authors.find(
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
        
        if query:
            results = list(db.books.find(query))
            
            for book in results:
                author = db.authors.find_one({'_id': book.get('author_id')})
                book['author_name'] = author['name'] if author else 'Unknown'
    
    return render_template('search.html', 
                         results=results, 
                         search_type=search_type)

if __name__ == '__main__':
    app.run(debug=True)
