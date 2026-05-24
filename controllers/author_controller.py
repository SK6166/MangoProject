from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database.connection import DatabaseConnection
from services.author_service import AuthorService
from middleware.auth import login_required, permission_required
from pymongo.errors import OperationFailure, PyMongoError

author_controller = Blueprint('author_controller', __name__)

def get_author_service():
    conn = DatabaseConnection.get_connection(session['db_username'], session['db_password'])
    return AuthorService(conn.db)

@author_controller.route('/authors')
@login_required
@permission_required('read')
def authors_list():
    try:
        service = get_author_service()
        authors = service.get_all_with_book_count()
        return render_template('authors.html', authors=authors)
    except OperationFailure as e:
        flash(str(e), 'danger')
        return redirect(url_for('index'))

@author_controller.route('/authors/add', methods=['POST'])
@login_required
@permission_required('write')
def add_author():
    try:
        service = get_author_service()
        service.add(
            name=request.form['name'],
            country=request.form.get('country'),
            birth_year=request.form.get('birth_year')
        )
        flash('Автор успешно добавлен', 'success')
    except OperationFailure as e:
        flash(str(e), 'danger')
    except PyMongoError as e:
        flash(f'Ошибка БД: {str(e)}', 'danger')
    return redirect(url_for('author_controller.authors_list'))

@author_controller.route('/authors/update/<string:author_id>', methods=['POST'])
@login_required
@permission_required('write')
def update_author(author_id):
    try:
        service = get_author_service()
        service.update(
            author_id=author_id,
            name=request.form['name'],
            country=request.form.get('country'),
            birth_year=request.form.get('birth_year')
        )
        flash('Автор успешно обновлен', 'success')
    except OperationFailure as e:
        flash(str(e), 'danger')
    except PyMongoError as e:
        flash(f'Ошибка БД: {str(e)}', 'danger')
    return redirect(url_for('author_controller.authors_list'))

@author_controller.route('/authors/delete/<string:author_id>')
@login_required
@permission_required('delete')
def delete_author(author_id):
    try:
        service = get_author_service()
        service.delete(author_id)
        flash('Автор и все его книги успешно удалены', 'success')
    except OperationFailure as e:
        flash(str(e), 'danger')
    except PyMongoError as e:
        flash(f'Ошибка БД: {str(e)}', 'danger')
    return redirect(url_for('author_controller.authors_list'))