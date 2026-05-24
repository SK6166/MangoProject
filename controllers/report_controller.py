from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database.connection import DatabaseConnection
from services.report_service import ReportService
from services.book_service import BookService
from middleware.auth import login_required, permission_required
from pymongo.errors import OperationFailure

report_controller = Blueprint('report_controller', __name__)

def get_report_service():
    conn = DatabaseConnection.get_connection(session['db_username'], session['db_password'])
    return ReportService(conn.db)

@report_controller.route('/report/books_by_genre')
@login_required
@permission_required('read')
def report_books_by_genre():
    try:
        service = get_report_service()
        data = service.books_by_genre()
        return render_template('report_books_by_genre.html', data=data)
    except OperationFailure as e:
        flash(str(e), 'danger')
        return redirect(url_for('index'))

@report_controller.route('/report/books_by_year', methods=['GET', 'POST'])
@login_required
@permission_required('read')
def report_books_by_year():
    try:
        service = get_report_service()
        if request.method == 'POST':
            results, summary, search_params, all_genres = service.books_by_year(
                year_from=request.form.get('year_from'),
                year_to=request.form.get('year_to'),
                genre=request.form.get('genre'),
                available=request.form.get('available')
            )
        else:
            results = []
            summary = {}
            search_params = {}
            all_genres = BookService(
                DatabaseConnection.get_connection(session['db_username'], session['db_password']).db
            ).db.books.distinct('genre')

        return render_template('report_books_by_year.html',
                             results=results,
                             summary=summary,
                             search_params=search_params,
                             all_genres=all_genres)
    except OperationFailure as e:
        flash(str(e), 'danger')
        return redirect(url_for('index'))

@report_controller.route('/report/books_availability')
@login_required
@permission_required('read')
def report_books_availability():
    try:
        service = get_report_service()
        available_count, unavailable_count, total, genre_availability = service.books_availability()
        return render_template('report_books_availability.html',
                             available_count=available_count,
                             unavailable_count=unavailable_count,
                             total=total,
                             genre_availability=genre_availability)
    except OperationFailure as e:
        flash(str(e), 'danger')
        return redirect(url_for('index'))

@report_controller.route('/report/authors_activity')
@login_required
@permission_required('read')
def report_authors_activity():
    try:
        service = get_report_service()
        data = service.authors_activity()
        return render_template('report_authors_activity.html', data=data)
    except OperationFailure as e:
        flash(str(e), 'danger')
        return redirect(url_for('index'))

@report_controller.route('/report/authors_by_country')
@login_required
@permission_required('read')
def report_authors_by_country():
    try:
        service = get_report_service()
        data = service.authors_by_country()
        return render_template('report_authors_by_country.html', data=data)
    except OperationFailure as e:
        flash(str(e), 'danger')
        return redirect(url_for('index'))

@report_controller.route('/report/authors_by_era', methods=['GET', 'POST'])
@login_required
@permission_required('read')
def report_authors_by_era():
    try:
        service = get_report_service()
        if request.method == 'POST':
            results, summary, search_params, all_countries = service.authors_by_era(
                birth_from=request.form.get('birth_from'),
                birth_to=request.form.get('birth_to'),
                country=request.form.get('country')
            )
        else:
            results = []
            summary = {}
            search_params = {}
            all_countries = DatabaseConnection.get_connection(
                session['db_username'], session['db_password']
            ).db.authors.distinct('country')

        return render_template('report_authors_by_era.html',
                             results=results,
                             summary=summary,
                             search_params=search_params,
                             all_countries=all_countries)
    except OperationFailure as e:
        flash(str(e), 'danger')
        return redirect(url_for('index'))

@report_controller.route('/search', methods=['GET', 'POST'])
@login_required
@permission_required('read')
def search():
    try:
        conn = DatabaseConnection.get_connection(session['db_username'], session['db_password'])
        book_service = BookService(conn.db)

        if request.method == 'POST':
            results, search_type = book_service.search(
                search_term=request.form.get('search'),
                search_field=request.form.get('search_field', 'title'),
                year_from=request.form.get('year_from')
            )
        else:
            results = []
            search_type = 'simple'

        return render_template('search.html', results=results, search_type=search_type)
    except OperationFailure as e:
        flash(str(e), 'danger')
        return redirect(url_for('index'))