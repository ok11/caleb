import http
import logging
import traceback

from flask import Blueprint, abort, request, jsonify

from app.frontend.api.model import *
from app.core.model import *

api = Blueprint('api', __name__, url_prefix='/api')

book_schema = BookSchema(strict=True)
books_schema = BookSchema(many=True, strict=True)
author_schema = AuthorSchema(strict=True)
authors_schema = AuthorSchema(many=True, strict=True)
series_schema = SeriesSchema(strict=True)


@api.route("/books/", methods=["GET"])
def get_books():
    try:
        books = Book.query.all()
        response = books_schema.jsonify(books)
        response.status_code = http.HTTPStatus.OK
        response.headers['content-type'] = 'application/json'
        return response
    except Exception as e:
        logging.exception(e, exc_info=True)
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR, e)


@api.route("/books/", methods=["POST"])
def create_book():
    try:
        j = request.get_json()
        data, err = book_schema.load(j)
        book_dict = {k: data[k] for (k, data[k]) in data.items() if k not in [
                'authors', 'languages', 'tags', 'identifiers', 'series'
            ]
        } # TODO: fill in with relationships from Book
        book = Book(**book_dict)
        for author in data.get('authors', []):
            book.authors.append(Author(**author))
        for language in data.get('languages', []):
            book.languages.append(Language(**language))
        for tag in data.get('tags', []):
            book.tags.append(Tag(**tag))
        for ident in data.get('identifiers', []):
            book.identifiers.append(Identifier(**ident))
        for series in data.get('series', []):
            book.series.append(Series(**series))
        book.save()

        response = book_schema.jsonify(book)
        response.status_code = http.HTTPStatus.CREATED
        response.headers['location'] = '/api/books/{}'.format(book.id)
        response.headers['content-type'] = 'application/json'
        return response
    except ValidationError as e:
        logging.exception(e, exc_info=True)
        abort(http.HTTPStatus.BAD_REQUEST, e)
    except Exception as e:
#        trace = traceback.format_exc()
        logging.exception(e, exc_info=True)
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR, e)


@api.route("/books/<string:id>", methods=["GET"])
def get_book(id):
    try:
        book = Book.query.get(id)
        if book:
            response = book_schema.jsonify(book)
            response.status_code = http.HTTPStatus.OK
            response.headers['content-type'] = 'application/json'
            return response
        else:
            return ('', http.HTTPStatus.NOT_FOUND)
    except Exception as e:
        logging.exception(e, exc_info=True)
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR, e)


@api.route("/books/<string:id>", methods=["PUT"])
def update_book(id):
    try:
        book = Book.query.get(id)
        if book:
            j = request.get_json()
            data, err = book_schema.load(j)
            book.update(**data)
            book.save()

            response = book_schema.jsonify(book)
            response.status_code = http.HTTPStatus.OK
            response.headers['content-type'] = 'application/json'
            return response
        else:
            logging.debug("Book not found: {}".format(id))
            return ('', http.HTTPStatus.NOT_FOUND)
    except Exception as e:
        logging.exception(e, exc_info=True)
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR, e)


@api.route("/books/<string:id>/authors/", methods=["GET"])
def get_book_authors(id):
    try:
        book = Book.query.get(id)
        if book:
            response = authors_schema.jsonify(book.authors)
            response.status_code = http.HTTPStatus.OK
            response.headers['content-type'] = 'application/json'
            return response
        else:
            logging.debug("Book not found: {}".format(id))
            return ('', http.HTTPStatus.NOT_FOUND)
    except Exception as e:
        logging.exception(e, exc_info=True)
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR, e)


@api.route("/books/<string:id>/authors/", methods=["POST"])
def create_book_author(id):
    try:
        book = Book.query.get(id)
        if book:
            j = request.get_json()
            data, err = author_schema.load(j)
            author = Author(**data)
            author.append(book)
            author.save()

            response = author_schema.jsonify(author)
            response.status_code = http.HTTPStatus.CREATED
            response.headers['location'] = '/api/books/{}/authors/{}'.format(book.id, author.id)
            response.headers['content-type'] = 'application/json'
            return response
        else:
            logging.debug("Book not found: {}".format(id))
            return ('', http.HTTPStatus.NOT_FOUND)
    except Exception as e:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR, e)


@api.route("/authors/", methods=["GET"])
def get_authors():
    try:
        authors = Author.query.all()
        response = authors_schema.jsonify(authors)
        response.status_code = http.HTTPStatus.OK
        response.headers['content-type'] = 'application/json'
        return response
    except Exception as e:
        logging.exception(e, exc_info=True)
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR, e)


@api.route("/authors/", methods=["POST"])
def create_author():
    try:
        j = request.get_json()
        data, err = author_schema.load(j)
        author = Author(**data)
        author.save()

        response = book_schema.jsonify(author)
        response.status_code = http.HTTPStatus.CREATED
        response.headers['location'] = '/api/books/{}'.format(author.id)
        response.headers['content-type'] = 'application/json'
        return response
    except ValidationError as e:
        logging.exception(e, exc_info=True)
        abort(http.HTTPStatus.BAD_REQUEST, e)
    except Exception as e:
        logging.exception(e, exc_info=True)
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR, e)


@api.route("/authors/<string:id>", methods=["GET"])
def get_author(id):
    try:
        author = Author.query.get(id)
        if author:
            response = author_schema.jsonify(author)
            response.status_code = http.HTTPStatus.OK
            response.headers['content-type'] = 'application/json'
            return response
        else:
            logging.debug("Author not found: {}".format(id))
            return ('', http.HTTPStatus.NOT_FOUND)
    except Exception as e:
        logging.exception(e, exc_info=True)
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR, e)


@api.route("/authors/<string:id>", methods=["PUT"])
def update_author(id):
    try:
        author = Author.query.get(id)
        if author:
            j = request.get_json()
            data, err = author_schema.load(j)
            author.update(**data)
            # author.name = data['name']
            # author.sort = data['sort']
            # author.link = data['link']
            author.save()

            response = author_schema.jsonify(author)
            response.status_code = http.HTTPStatus.OK
            response.headers['content-type'] = 'application/json'
            return response
        else:
            logging.debug("Author not found: {}".format(id))
            return ('', http.HTTPStatus.NOT_FOUND)
    except Exception as e:
        logging.exception(e, exc_info=True)
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR, e)


@api.route("/series/", methods=["GET"])
def get_all_series():
    try:
        series = Series.query.all()
        response = series_schema.jsonify(series)
        response.status_code = http.HTTPStatus.OK
        response.headers['content-type'] = 'application/json'
        return response
    except Exception as e:
        logging.exception(e, exc_info=True)
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR, e)


@api.route("/series/", methods=["POST"])
def create_series():
    try:
        j = request.get_json()
        data, err = series_schema.load(j)
        series = Series(**data)
        series.save()

        response = book_schema.jsonify(series)
        response.status_code = http.HTTPStatus.CREATED
        response.headers['location'] = '/api/books/{}'.format(series.id)
        response.headers['content-type'] = 'application/json'
        return response
    except ValidationError as e:
        logging.exception(e, exc_info=True)
        abort(http.HTTPStatus.BAD_REQUEST, e)
    except Exception as e:
        logging.exception(e, exc_info=True)
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR, e)


@api.route("/series/<string:id>", methods=["GET"])
def get_series(id):
    try:
        series = Series.query.get(id)
        if series:
            response = series_schema.jsonify(series)
            response.status_code = http.HTTPStatus.OK
            response.headers['content-type'] = 'application/json'
            return response
        else:
            logging.debug("Series not found: {}".format(id))
            return ('', http.HTTPStatus.NOT_FOUND)
    except Exception as e:
        logging.exception(e, exc_info=True)
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR, e)


@api.route("/series/<string:id>", methods=["PUT"])
def update_series(id):
    try:
        series = Series.query.get(id)
        if series:
            j = request.get_json()
            data, err = series_schema.load(j)
            series.update(**data)
            # series.name = data['name']
            # series.sort = data['sort']
            series.save()

            response = series_schema.jsonify(series)
            response.status_code = http.HTTPStatus.OK
            response.headers['content-type'] = 'application/json'
            return response
        else:
            logging.debug("Series not found: {}".format(id))
            return ('', http.HTTPStatus.NOT_FOUND)
    except Exception as e:
        logging.exception(e, exc_info=True)
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR, e)


@api.route("/series/<string:id>/books", methods=["GET"])
def get_series_books(id):
    try:
        series = Series.query.get(id)
        if series:
            books = series.books()
            response = books_schema.jsonify(books)
            response.status_code = http.HTTPStatus.OK
            response.headers['content-type'] = 'application/json'
            return response
        else:
            logging.debug("Series not found: {}".format(id))
            return ('', http.HTTPStatus.NOT_FOUND)
    except Exception as e:
        logging.exception(e, exc_info=True)
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR, e)

