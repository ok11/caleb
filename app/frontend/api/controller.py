import http

from flask import Blueprint, abort, request, jsonify

from app.frontend.api.model import *
from app.core.model import *

api = Blueprint('api', __name__, url_prefix='/api')

book_schema = BookSchema(strict=True)
books_schema = BookSchema(many=True, strict=True)
author_schema = AuthorSchema(strict=True)
authors_schema = AuthorSchema(many=True, strict=True)

@api.route("/books/", methods = ["GET"])
def get_books():
    try:
        books = Book.query.all()
        response = books_schema.jsonify(books)
        response.status_code = http.HTTPStatus.OK
        response.headers['content-type'] = 'application/json'
        return response
    except Exception as e:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR, e)

@api.route("/books/", methods = ["POST"])
def create_book():
    try:
        j = request.get_json()
        data, err = book_schema.load(j)
        book = Book(**data)
        for author in data.get('authors', []):
            book.authors.append(Author(**author))
        for language in data.get('languages', []):
            book.languages.append(Language(**language))
        for tag in data.get('tags', []):
            book.tags.append(Tag(**tag))
        for ident in data.get('identifiers', []):
            book.identifiers.append(Identifier(**ident))
        book.save()

        response = book_schema.jsonify(book)
        response.status_code = http.HTTPStatus.CREATED
        response.headers['location'] = '/api/books/{}'.format(book.id)
        response.headers['content-type'] = 'application/json'
        return response
    except Exception as e:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR, e)


@api.route("/books/<string:id>", methods = ["GET"])
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
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR, e)

@api.route("/books/<string:id>", methods = ["PUT"])
def update_book(id):
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
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR, e)


@api.route("/books/<string:id>/authors/", methods = ["GET"])
def get_book_authors(id):
    try:
        book = Book.query.get(id)
        if book:
            response = authors_schema.jsonify(book.authors)
            response.status_code = http.HTTPStatus.OK
            response.headers['content-type'] = 'application/json'
            return response
        else:
            return ('', http.HTTPStatus.NOT_FOUND)
    except Exception as e:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR, e)


@api.route("/books/<string:id>/authors/", methods = ["POST"])
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
            return ('', http.HTTPStatus.NOT_FOUND)
    except Exception as e:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR, e)

