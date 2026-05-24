from flask import Flask, render_template, session
from config import Config
from database.connection import DatabaseConnection
from controllers.auth_controller import auth_controller
from controllers.book_controller import book_controller
from controllers.author_controller import author_controller
from controllers.report_controller import report_controller

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

app.register_blueprint(auth_controller)
app.register_blueprint(book_controller)
app.register_blueprint(author_controller)
app.register_blueprint(report_controller)

@app.route('/')
def index():
    db_info = {}
    if 'db_username' in session and 'db_password' in session:
        try:
            conn = DatabaseConnection.get_connection(session['db_username'], session['db_password'])
            if conn and conn.db is not None:
                books_count = conn.db.books.count_documents({})
                authors_count = conn.db.authors.count_documents({})
                db_info = {
                    'books_count': books_count,
                    'authors_count': authors_count,
                    'connected': True
                }
        except Exception as e:
            db_info = {'connected': False, 'error': str(e)}
    else:
        db_info = {'connected': False}

    return render_template('index.html', db_info=db_info)

if __name__ == '__main__':
    app.run(debug=True)