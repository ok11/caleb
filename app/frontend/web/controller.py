import http

from flask import Blueprint, request, abort, jsonify

from app.core.model import *

web = Blueprint('web', __name__, url_prefix='/web')

@web.route("/books/", methods = ["GET"])
def get_books():
    try:
        return jsonify(Book.query.all())
    except Exception as e:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR, e)
