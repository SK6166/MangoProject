from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database.connection import DatabaseConnection
from services.book_service import BookService
from middleware.auth import login_required, permission_required
from pymongo.errors import OperationFailure, PyMongoError

book_controller = Blueprint('book_controller', __name__)

def get_book_service():
    conn = DatabaseConnection.get_connection(session['db_username'], session['db_password'])
    return BookService(conn.db)

@book_controller.route('/books')
@login_required
@permission_required('read')
def books_list():
    try:
        service = get_book_service()
        books = service.get_all_with_authors()
        authors = service.get_all_authors()
        return render_template('books.html', books=books, authors=authors)
    except OperationFailure as e:
        flash(str(e), 'danger')
        return redirect(url_for('index'))

@book_controller.route('/books/add', methods=['POST'])
@login_required
@permission_required('write')
def add_book():
    try:
        service = get_book_service()
        service.add(
            title=request.form['title'],
            year=request.form['year'],
            author_id=request.form['author_id'],
            genre=request.form.get('genre'),
            available='available' in request.form
        )
        flash('Книга успешно добавлена', 'success')
    except OperationFailure as e:
        flash(str(e), 'danger')
    except PyMongoError as e:
        flash(f'Ошибка БД: {str(e)}', 'danger')
    return redirect(url_for('book_controller.books_list'))

@book_controller.route('/books/update/<string:book_id>', methods=['POST'])
@login_required
@permission_required('write')
def update_book(book_id):
    try:
        service = get_book_service()
        service.update(
            book_id=book_id,
            title=request.form['title'],
            year=request.form['year'],
            genre=request.form.get('genre'),
            available='available' in request.form
        )
        flash('Книга успешно обновлена', 'success')
    except OperationFailure as e:
        flash(str(e), 'danger')
    except PyMongoError as e:
        flash(f'Ошибка БД: {str(e)}', 'danger')
    return redirect(url_for('book_controller.books_list'))

@book_controller.route('/books/delete/<string:book_id>')
@login_required
@permission_required('delete')
def delete_book(book_id):
    try:
        service = get_book_service()
        service.delete(book_id)
        flash('Книга успешно удалена', 'success')
    except OperationFailure as e:
        flash(str(e), 'danger')
    except PyMongoError as e:
        flash(f'Ошибка БД: {str(e)}', 'danger')
    return redirect(url_for('book_controller.books_list'))