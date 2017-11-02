from datetime import datetime
from app.data import db


def ts():
    return datetime.utcnow().isoformat(' ')


class BaseModel(db.Model):

    __abstract__ = True

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


books_authors_link = db.Table('books_authors_link', db.Model.metadata,
    db.Column('book', db.Integer, db.ForeignKey('books.id'), primary_key=True),
    db.Column('author', db.Integer, db.ForeignKey('authors.id'), primary_key=True)
)

books_tags_link = db.Table('books_tags_link', db.Model.metadata,
    db.Column('book', db.Integer, db.ForeignKey('books.id'), primary_key=True),
    db.Column('tag', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

books_series_link = db.Table('books_series_link', db.Model.metadata,
    db.Column('book', db.Integer, db.ForeignKey('books.id'), primary_key=True),
    db.Column('series', db.Integer, db.ForeignKey('series.id'), primary_key=True)
)

books_ratings_link = db.Table('books_ratings_link', db.Model.metadata,
    db.Column('book', db.Integer, db.ForeignKey('books.id'), primary_key=True),
    db.Column('rating', db.Integer, db.ForeignKey('ratings.id'), primary_key=True)
)

books_languages_link = db.Table('books_languages_link', db.Model.metadata,
    db.Column('book', db.Integer, db.ForeignKey('books.id'), primary_key=True),
    db.Column('lang_code', db.Integer, db.ForeignKey('languages.id'), primary_key=True)
)

books_publishers_link = db.Table('books_publishers_link', db.Model.metadata,
    db.Column('book', db.Integer, db.ForeignKey('books.id'), primary_key=True),
    db.Column('publisher', db.Integer, db.ForeignKey('publishers.id'), primary_key=True)
)

class Identifier(BaseModel):

    __tablename__ = 'identifiers'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    val = db.Column(db.String)
    book = db.Column(db.Integer, db.ForeignKey('books.id'))

    # def __init__(self, val, id_type, book):
    #     self.val = val
    #     self.type = id_type
    #     self.book = book
    #
    def formatType(self):
        if self.type == "amazon":
            return u"Amazon"
        elif self.type == "isbn":
            return u"ISBN"
        elif self.type == "doi":
            return u"DOI"
        elif self.type == "goodreads":
            return u"Goodreads"
        elif self.type == "google":
            return u"Google Books"
        elif self.type == "kobo":
            return u"Kobo"
        elif self.type == "ozon":
            return u"Ozon"
        else:
            return self.type

    def __repr__(self):
        if self.type == "amazon":
            return u"https://amzn.com/{0}".format(self.val)
        elif self.type == "isbn":
            return u"http://www.worldcat.org/isbn/{0}".format(self.val)
        elif self.type == "doi":
            return u"http://dx.doi.org/{0}".format(self.val)
        elif self.type == "goodreads":
            return u"http://www.goodreads.com/book/show/{0}".format(self.val)
        elif self.type == "douban":
            return u"https://book.douban.com/subject/{0}".format(self.val)
        elif self.type == "google":
            return u"https://books.google.com/books?id={0}".format(self.val)
        elif self.type == "kobo":
            return u"https://www.kobo.com/ebook/{0}".format(self.val)
        elif self.type == "ozon":
            return u"https://ozon.ru/{0}".format(self.val)
        else:
            return u""


class Comment(BaseModel):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    book = db.Column(db.Integer, db.ForeignKey('books.id'))

    # def __init__(self, text, book):
    #     self.text = text
    #     self.book = book

    def __repr__(self):
        return u"<Comment({0})>".format(self.text)


class Tag(BaseModel):

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)

    # def __init__(self, name):
    #     self.name = name

    def __repr__(self):
        return u"<Tag('{0})>".format(self.name)


class Author(BaseModel):

    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    sort = db.Column(db.String)
    link = db.Column(db.String)

    # def __init__(self, name, sort, link):
    #     self.name = name
    #     self.sort = sort
    #     self.link = link

    def __repr__(self):
        return u"<Author('{0},{1} {2}')>".format(self.name, self.sort, self.link)


class Series(BaseModel):

    __tablename__ = 'series'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    sort = db.Column(db.String)

    # def __init__(self, name, sort):
    #     self.name = name
    #     self.sort = sort

    def __repr__(self):
        return u"<Series('{0}, {1}')>".format(self.name, self.sort)


class Rating(BaseModel):

    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)

    # def __init__(self, rating):
    #     self.rating = rating

    def __repr__(self):
        return u"<Rating('{0}')>".format(self.rating)


class Language(BaseModel):

    __tablename__ = 'languages'

    id = db.Column(db.Integer, primary_key=True)
    lang_code = db.Column(db.String)
    #
    # def __init__(self, lang_code):
    #     self.lang_code = lang_code

    def __repr__(self):
        return u"<Language('{0}')>".format(self.lang_code)


class Publisher(BaseModel):

    __tablename__ = 'publishers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    sort = db.Column(db.String)

    # def __init__(self, name, sort):
    #     self.name = name
    #     self.sort = sort

    def __repr__(self):
        return u"<Publisher('{0}, {1}')>".format(self.name, self.sort)



class Data(BaseModel):

    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key=True)
    book = db.Column(db.Integer, db.ForeignKey('books.id'))
    format = db.Column(db.String)
    uncompressed_size = db.Column(db.Integer)
    name = db.Column(db.String)

    # def __init__(self, book, book_format, uncompressed_size, name):
    #     self.book = book
    #     self.format = book_format
    #     self.uncompressed_size = uncompressed_size
    #     self.name = name

    def __repr__(self):
        return u"<Data('{0}, {1} {2} {3}')>".format(self.book, self.format, self.uncompressed_size, self.name)


class Book(BaseModel):

    __tablename__ = 'books'

    DEFAULT_PUBDATE = "0101-01-01 00:00:00+00:00"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    sort = db.Column(db.String)
    author_sort = db.Column(db.String)
    timestamp = db.Column(db.String, default=ts)
    pubdate = db.Column(db.String)
    series_index = db.Column(db.String)
    last_modified = db.Column(db.String, default=ts, onupdate=ts)
    path = db.Column(db.String)
    has_cover = db.Column(db.Integer)
    uuid = db.Column(db.String)

    authors = db.relationship('Author', secondary=books_authors_link, backref='books')
    tags = db.relationship('Tag', secondary=books_tags_link, backref='books')
    comments = db.relationship('Comment', backref='books')
    data = db.relationship('Data', backref='books')
    series = db.relationship('Series', secondary=books_series_link, backref='books')
    ratings = db.relationship('Rating', secondary=books_ratings_link, backref='books')
    languages = db.relationship('Language', secondary=books_languages_link, backref='books')
    publishers = db.relationship('Publisher', secondary=books_publishers_link, backref='books')
    identifiers = db.relationship('Identifier', backref='books')


    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.sort = kwargs.get('sort', '')
        self.author_sort = kwargs.get('author_sort', '')
        self.pubdate = kwargs.get('pubdate', '')
        self.series_index = kwargs.get('series_index', '0')
        self.path = kwargs.get('path')
        self.has_cover = kwargs.get('has_cover', 0)

    def __repr__(self):
        return u"<Books('{0}, {1} {2} {3} {4} {5} {6} {7} {8}')>".format(
            self.title, self.sort, self.author_sort,
            self.timestamp, self.pubdate, self.series_index,
            self.last_modified, self.path, self.has_cover
        )


class Custom_Column(BaseModel):

    __tablename__ = 'custom_columns'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String)
    name = db.Column(db.String)
    datatype = db.Column(db.String)
    mark_for_delete = db.Column(db.Boolean)
    editable = db.Column(db.Boolean)
    display = db.Column(db.String)
    is_multiple = db.Column(db.Boolean)
    normalized = db.Column(db.Boolean)

