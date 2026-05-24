import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecretkey123')
    MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
    MONGO_PORT = os.environ.get('MONGO_PORT', '27017')
    MONGO_DB = os.environ.get('MONGO_DB', 'library_db')
    MONGO_AUTH_SOURCE = os.environ.get('MONGO_AUTH_SOURCE', 'library_db')
    SERVER_TIMEOUT = 5000
    CONNECT_TIMEOUT = 5000

    USERS = {
        'admin': {
            'username': 'admin_user',
            'password': 'admin123',
            'role': 'admin',
            'permissions': ['read', 'write', 'delete']
        },
        'editor': {
            'username': 'read_write_user',
            'password': 'rw123',
            'role': 'editor',
            'permissions': ['read', 'write']
        },
        'viewer': {
            'username': 'read_only_user',
            'password': 'read123',
            'role': 'viewer',
            'permissions': ['read']
        }
    }