from pymongo import MongoClient, ASCENDING, TEXT
from pymongo.errors import CollectionInvalid, OperationFailure

client = MongoClient('mongodb://localhost:27017')
db = client['library_db']

print("Создание коллекций...")
try:
    db.create_collection('books')
    db.create_collection('authors')
    print("Коллекции 'books' и 'authors' созданы.")
except CollectionInvalid:
    print("Коллекции уже существуют.")

print("Создание индексов...")
db.books.create_index([('title', TEXT), ('genre', ASCENDING)]) 
db.books.create_index([('author_id', ASCENDING)])
db.books.create_index([('year', ASCENDING)])
db.books.create_index([('tags', ASCENDING)])

db.authors.create_index([('name', TEXT)])
db.authors.create_index([('country', ASCENDING)])
db.authors.create_index([('birth_year', ASCENDING)])

print("Индексы созданы.")
try:
    db.command('createUser', 'read_only_user', pwd='read123', roles=[{'role': 'read', 'db': 'library_db'}])
    db.command('createUser', 'read_write_user', pwd='rw123', roles=[{'role': 'readWrite', 'db': 'library_db'}])
    db.command('createUser', 'admin_user', pwd='admin123', roles=[{'role': 'dbAdmin', 'db': 'library_db'}, {'role': 'userAdmin', 'db': 'library_db'}, {'role': 'readWrite', 'db': 'library_db'}])
except Exception as e:
    print("Ошибка при создании пользователей")
    print(e)

print("Пользователи созданы:")
print("1. read_only_user / read123 (Только чтение)")
print("2. read_write_user / rw123 (Чтение и запись)")
print("3. admin_user / admin123 (Полный доступ к БД)")
