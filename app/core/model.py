from datetime import datetime
from app.data import db
from sqlalchemy.ext.associationproxy import association_proxy

def ts():
    return datetime.utcnow().isoformat(' ')


class Dictable:
    def to_dict(self):
        return self.__dict__


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

class BaseIdentifier(Dictable):

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.val = kwargs.get('val')
        self.type = kwargs.get('type')

        self.book = {}


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


class Identifier(BaseModel, BaseIdentifier):

    __tablename__ = 'identifiers'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    val = db.Column(db.String)

    book = db.Column(db.Integer, db.ForeignKey('books.id'))


class BaseComment(Dictable):

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.text = kwargs.get('text')

        self.book = {}

    def __repr__(self):
        return u"<Comment({0})>".format(self.text)


class Comment(BaseModel, BaseComment):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    book = db.Column(db.Integer, db.ForeignKey('books.id'))


class BaseTag(Dictable):

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name')

    def __repr__(self):
        return u"<Tag('{0})>".format(self.name)


class Tag(BaseModel, BaseTag):

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)


class BaseAuthor(Dictable):

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name')
        self.sort = kwargs.get('sort', self.name)
        self.link = kwargs.get('link', '')

    def __repr__(self):
        return u"<Author('{0},{1} {2}')>".format(self.name, self.sort, self.link)


class Author(BaseModel, BaseAuthor):

    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    sort = db.Column(db.String)
    link = db.Column(db.String)


class BaseSeries(Dictable):

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name')
        self.sort = kwargs.get('sort', self.name)

    def __repr__(self):
        return u"<Series('{0}, {1}')>".format(self.name, self.sort)

class Series(BaseModel, BaseSeries):

    __tablename__ = 'series'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    sort = db.Column(db.String)


class BaseRating(Dictable):

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.rating = kwargs.get('rating')

    def __repr__(self):
        return u"<Rating('{0}')>".format(self.rating)


class Rating(BaseModel, BaseRating):

    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)


class BaseLanguage(Dictable):

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.lang_code = kwargs.get('lang_code')

    def __repr__(self):
        return u"<Language('{0}')>".format(self.lang_code)


class Language(BaseModel, BaseLanguage):

    __tablename__ = 'languages'

    id = db.Column(db.Integer, primary_key=True)
    lang_code = db.Column(db.String)


class BasePublisher(Dictable):

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name')
        self.sort = kwargs.get('sort', self.name)

    def __repr__(self):
        return u"<Publisher('{0}, {1}')>".format(self.name, self.sort)


class Publisher(BaseModel, BasePublisher):

    __tablename__ = 'publishers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    sort = db.Column(db.String)


class BaseData(Dictable):

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.format = kwargs.get('format')
        self.uncompressed_size = kwargs.get('uncompressed_size')
        self.name = kwargs.get('name')

        self.book = {}

    def __repr__(self):
        return u"<Data('{0}, {1} {2} {3}')>".format(
            self.book, self.format, self.uncompressed_size, self.name
        )


class Data(BaseModel, BaseData):

    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key=True)
    book = db.Column(db.Integer, db.ForeignKey('books.id'))
    format = db.Column(db.String)
    uncompressed_size = db.Column(db.Integer)
    name = db.Column(db.String)


class BaseBook(Dictable):

    DEFAULT_PUBDATE = "0101-01-01 00:00:00+00:00"

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.title = kwargs.get('title')
        self.sort = kwargs.get('sort', '')
        self.author_sort = kwargs.get('author_sort', '')
        self.pubdate = kwargs.get('pubdate', BaseBook.DEFAULT_PUBDATE)
        self.series_index = kwargs.get('series_index', '0')
        self.path = kwargs.get('path')
        self.has_cover = kwargs.get('has_cover', 0)
        self.timestamp = kwargs.get('timestamp', None)
        self.last_modified = kwargs.get('last_modified', None)

        self.authors = []
        self.tags = []
        self.identifiers = []
        self.ratings = []
        self.languages = []
        self.series = []

    def __repr__(self):
        return u"<Book ('{0} {1}, {2} {3} {4} {5} {6}')>".format(
            self.title, self.sort, self.author_sort,
            self.pubdate, self.series_index,
            self.path, self.has_cover
        )


class Book(BaseModel, BaseBook):

    __tablename__ = 'books'

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
    series = db.relationship('Series', secondary=books_series_link, backref='books')
    ratings = db.relationship('Rating', secondary=books_ratings_link, backref='books')
    languages = db.relationship('Language', secondary=books_languages_link, backref='books')
    publishers = db.relationship('Publisher', secondary=books_publishers_link, backref='books')

    comments = db.relationship('Comment', backref='books')
    data = db.relationship('Data', backref='books')
    identifiers = db.relationship('Identifier', backref='books')

    # authors = association_proxy('_authors', 'name')
    # tags = association_proxy('_tags', 'name', creator=lambda t: Tag(**t))
    # languages = association_proxy('_languages', 'lang_code')
    # series = association_proxy('_series', 'name')
    # ratings = association_proxy('_ratings', 'rating')
    # publishers = association_proxy('_publishers', 'name')
    #
    # identifiers = association_proxy('_identifiers', 'val')

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

