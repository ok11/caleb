from app.data import db


def common_filters():
    if current_user.filter_language() != "all":
        lang_filter = db.Books.languages.any(db.Languages.lang_code == current_user.filter_language())
    else:
        lang_filter = true()
    content_rating_filter = false() if current_user.mature_content else \
        db.Books.tags.any(db.Tags.name.in_(config.mature_content_tags()))
    return and_(lang_filter, ~content_rating_filter)


# Fill indexpage with all requested data from database
def fill_indexpage(page, database, db_filter, order):
    if current_user.show_detail_random():
        random = db.session.query(db.Books).filter(common_filters())\
            .order_by(func.random()).limit(config.config_random_books)
    else:
        random = false
    off = int(int(config.config_books_per_page) * (page - 1))
    pagination = Pagination(page, config.config_books_per_page,
                            len(db.session.query(database)
                                .filter(db_filter).filter(common_filters()).all()))
    entries = db.session.query(database).filter(db_filter).filter(common_filters())\
        .order_by(order).offset(off).limit(config.config_books_per_page)
    return entries, random, pagination

def search(term):
    entries = []
    if term:
        term = term.strip().lower()
        db.session.connection().connection.connection.create_function("lower", 1, db.lcase)
        entries = db.session.query(db.Books).filter(db.or_(db.Books.tags.any(db.Tags.name.ilike("%" + term + "%")),
                                                           db.Books.series.any(db.Series.name.ilike("%" + term + "%")),
                                                           db.Books.authors.any(db.Authors.name.ilike("%" + term + "%")),
                                                           db.Books.publishers.any(
                                                               db.Publishers.name.ilike("%" + term + "%")),
                                                           db.Books.title.ilike("%" + term + "%"))) \
            .filter(common_filters()).all()
    return entries

