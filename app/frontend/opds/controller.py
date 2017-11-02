import http

from flask import Blueprint, request, abort, jsonify

from app.core.model import *

opds = Blueprint('opds', __name__, url_prefix='/opds')

@opds.route("/books/", methods = ["GET"])
def get_books():
    try:
        return jsonify(Book.guery.all())
    except Exception as e:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR, e)

