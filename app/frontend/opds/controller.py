import http

from flask import Blueprint, request, abort, jsonify, make_response, render_template

from app.core.model import *


opds = Blueprint('opds', __name__, url_prefix='/opds')


@opds.route("/books/", methods=["GET"])
def get_books():
    try:
        return jsonify(Book.guery.all())
    except Exception as e:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR, e)


@opds.route("/index/", methods=["GET"])
def feed_index():
    xml = render_template('index.xml')
    response = make_response(xml)
    response.headers["Content-Type"] = "application/atom+xml; charset=utf-8"
    return response


@opds.route("/osd/")
def feed_osd():
    xml = render_template('osd.xml', lang='de-DE')
    response = make_response(xml)
    response.headers["Content-Type"] = "application/xml; charset=utf-8"
    return response


@opds.route("/search/<query>")
def feed_cc_search(query):
    return feed_search(query.strip())


@opds.route("/search/", methods=["GET"])
def feed_normal_search():
    return feed_search(request.args.get("query").strip())


# def feed_search(term):
#         entriescount = len(entries) if len(entries) > 0 else 1
#         pagination = Pagination(1, entriescount, entriescount)
#         xml = render_title_template('feed.xml', searchterm=term, entries=entries, pagination=pagination)
#     else:
#         xml = render_title_template('feed.xml', searchterm="")
#     response = make_response(xml)
#     response.headers["Content-Type"] = "application/atom+xml; charset=utf-8"
#     return response
#
#
# @opds.route("/new/")
# def feed_new():
#     off = request.args.get("offset")
#     if not off:
#         off = 0
#     entries, __, pagination = fill_indexpage((int(off) / (int(config.config_books_per_page)) + 1),
#                                                  db.Books, True, db.Books.timestamp.desc())
#     xml = render_template('feed.xml', entries=entries, pagination=pagination)
#     response = make_response(xml)
#     response.headers["Content-Type"] = "application/atom+xml; charset=utf-8"
#     return response
#
#
# @app.route("/opds/discover")
# @requires_basic_auth_if_no_ano
# def feed_discover():
#     entries = db.session.query(db.Books).filter(common_filters()).order_by(func.random())\
#         .limit(config.config_books_per_page)
#     pagination = Pagination(1, config.config_books_per_page, int(config.config_books_per_page))
#     xml = render_title_template('feed.xml', entries=entries, pagination=pagination)
#     response = make_response(xml)
#     response.headers["Content-Type"] = "application/atom+xml; charset=utf-8"
#     return response
#
#
# @app.route("/opds/rated")
# @requires_basic_auth_if_no_ano
# def feed_best_rated():
#     off = request.args.get("offset")
#     if not off:
#         off = 0
#     entries, __, pagination = fill_indexpage((int(off) / (int(config.config_books_per_page)) + 1),
#                     db.Books, db.Books.ratings.any(db.Ratings.rating > 9), db.Books.timestamp.desc())
#     xml = render_title_template('feed.xml', entries=entries, pagination=pagination)
#     response = make_response(xml)
#     response.headers["Content-Type"] = "application/atom+xml; charset=utf-8"
#     return response
#
#
# @app.route("/opds/hot")
# @requires_basic_auth_if_no_ano
# def feed_hot():
#     off = request.args.get("offset")
#     if not off:
#         off = 0
#     all_books = ub.session.query(ub.Downloads, ub.func.count(ub.Downloads.book_id)).order_by(
#         ub.func.count(ub.Downloads.book_id).desc()).group_by(ub.Downloads.book_id)
#     hot_books = all_books.offset(off).limit(config.config_books_per_page)
#     entries = list()
#     for book in hot_books:
#         downloadBook = db.session.query(db.Books).filter(db.Books.id == book.Downloads.book_id).first()
#         if downloadBook:
#             entries.append(
#                 db.session.query(db.Books).filter(common_filters())
#                 .filter(db.Books.id == book.Downloads.book_id).first()
#             )
#         else:
#             ub.session.query(ub.Downloads).filter(book.Downloads.book_id == ub.Downloads.book_id).delete()
#             ub.session.commit()
#     numBooks = entries.__len__()
#     pagination = Pagination((int(off) / (int(config.config_books_per_page)) + 1), config.config_books_per_page, numBooks)
#     xml = render_title_template('feed.xml', entries=entries, pagination=pagination)
#     response = make_response(xml)
#     response.headers["Content-Type"] = "application/atom+xml; charset=utf-8"
#     return response
#
#
# @app.route("/opds/author")
# @requires_basic_auth_if_no_ano
# def feed_authorindex():
#     off = request.args.get("offset")
#     if not off:
#         off = 0
#     entries = db.session.query(db.Authors).join(db.books_authors_link).join(db.Books).filter(common_filters())\
#         .group_by('books_authors_link.author').order_by(db.Authors.sort).limit(config.config_books_per_page).offset(off)
#     pagination = Pagination((int(off) / (int(config.config_books_per_page)) + 1), config.config_books_per_page,
#                             len(db.session.query(db.Authors).all()))
#     xml = render_title_template('feed.xml', listelements=entries, folder='feed_author', pagination=pagination)
#     response = make_response(xml)
#     response.headers["Content-Type"] = "application/atom+xml; charset=utf-8"
#     return response
#
#
# @app.route("/opds/author/<int:book_id>")
# @requires_basic_auth_if_no_ano
# def feed_author(book_id):
#     off = request.args.get("offset")
#     if not off:
#         off = 0
#     entries, __, pagination = fill_indexpage((int(off) / (int(config.config_books_per_page)) + 1),
#                     db.Books, db.Books.authors.any(db.Authors.id == book_id), db.Books.timestamp.desc())
#     xml = render_title_template('feed.xml', entries=entries, pagination=pagination)
#     response = make_response(xml)
#     response.headers["Content-Type"] = "application/atom+xml; charset=utf-8"
#     return response
#
#
# @app.route("/opds/category")
# @requires_basic_auth_if_no_ano
# def feed_categoryindex():
#     off = request.args.get("offset")
#     if not off:
#         off = 0
#     entries = db.session.query(db.Tags).join(db.books_tags_link).join(db.Books).filter(common_filters())\
#         .group_by('books_tags_link.tag').order_by(db.Tags.name).offset(off).limit(config.config_books_per_page)
#     pagination = Pagination((int(off) / (int(config.config_books_per_page)) + 1), config.config_books_per_page,
#                             len(db.session.query(db.Tags).all()))
#     xml = render_title_template('feed.xml', listelements=entries, folder='feed_category', pagination=pagination)
#     response = make_response(xml)
#     response.headers["Content-Type"] = "application/atom+xml; charset=utf-8"
#     return response
#
#
# @app.route("/opds/category/<int:book_id>")
# @requires_basic_auth_if_no_ano
# def feed_category(book_id):
#     off = request.args.get("offset")
#     if not off:
#         off = 0
#     entries, __, pagination = fill_indexpage((int(off) / (int(config.config_books_per_page)) + 1),
#                     db.Books, db.Books.tags.any(db.Tags.id == book_id), db.Books.timestamp.desc())
#     xml = render_title_template('feed.xml', entries=entries, pagination=pagination)
#     response = make_response(xml)
#     response.headers["Content-Type"] = "application/atom+xml; charset=utf-8"
#     return response
#
#
# @app.route("/opds/series")
# @requires_basic_auth_if_no_ano
# def feed_seriesindex():
#     off = request.args.get("offset")
#     if not off:
#         off = 0
#     entries = db.session.query(db.Series).join(db.books_series_link).join(db.Books).filter(common_filters())\
#         .group_by('books_series_link.series').order_by(db.Series.sort).offset(off).all()
#     pagination = Pagination((int(off) / (int(config.config_books_per_page)) + 1), config.config_books_per_page,
#                             len(db.session.query(db.Series).all()))
#     xml = render_title_template('feed.xml', listelements=entries, folder='feed_series', pagination=pagination)
#     response = make_response(xml)
#     response.headers["Content-Type"] = "application/atom+xml; charset=utf-8"
#     return response
#
#
# @app.route("/opds/series/<int:book_id>")
# @requires_basic_auth_if_no_ano
# def feed_series(book_id):
#     off = request.args.get("offset")
#     if not off:
#         off = 0
#     entries, random, pagination = fill_indexpage((int(off) / (int(config.config_books_per_page)) + 1),
#                     db.Books, db.Books.series.any(db.Series.id == book_id),db.Books.series_index)
#     xml = render_title_template('feed.xml', entries=entries, pagination=pagination)
#     response = make_response(xml)
#     response.headers["Content-Type"] = "application/atom+xml; charset=utf-8"
#     return response
