import random
import factory

from app.core.model import *
from app import db

from faker.providers import BaseProvider

class CalebProvider(BaseProvider):
    def lang_code(self):
        lang_codes = ('en', 'ru', 'de')
        return random.choice(lang_codes)

    def ebook_id_type(self):
        id_types = ('isbn', 'amazon')
        return random.choice(id_types)

    def ebook_id_value(self, **kwargs):
        id_type = kwargs.get('ebook_id_type', 'isbn')
        if id_type == 'isbn':
            return factory.Faker('isbn13')
        else:
            return factory.Faker('isbn10')

    def ebook_format(self):
        ebook_formats = ('pdf', 'fb2', 'epub', 'mobi')
        return random.choice(ebook_formats)

factory.Faker.add_provider(CalebProvider)

class TagFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Tag
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('word')


class PublisherFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Publisher
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('company')
    sort = name


class LanguageFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Language
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    lang_code = factory.Faker('lang_code')


class RatingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Rating
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    rating = factory.Faker('pyint')


class AuthorFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Author
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('name')
    sort = name
    link = factory.Faker('uri')


class SeriesFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Series
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('word')
    sort = name


class BookFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Book
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    title = factory.Faker('sentence', nb_words=3)
    sort = title
    author_sort = factory.Faker('name')
    timestamp = factory.Faker('iso8601')
    pubdate = factory.Faker('iso8601')
    series_index = factory.Faker('pyint')
    last_modified = factory.Faker('iso8601')
    path = factory.Faker('file_path', depth=2)
    has_cover = factory.Faker('boolean')

    authors = factory.SubFactory(AuthorFactory)
    tags = factory.SubFactory(TagFactory)
    languages = factory.SubFactory(LanguageFactory)

#    identifiers = factory.RelatedFactory(IdentifierFactory)
#    comments = factory.RelatedFactory(CommentFactory)
#    data = factory.RelatedFactory(DataFactory)

class CommentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Comment
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    text = factory.Faker('sentence', nb_words=10)

    book = factory.SubFactory(BookFactory)


class IdentifierFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Identifier
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    type = factory.Faker('ebook_id_type')
    val = factory.Faker('ebook_id_value', ebook_id_type=type)

    book = factory.SubFactory(BookFactory)

class DataFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Data
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    format = factory.Faker('ebook_format')
    uncompressed_size = factory.Faker('pyint')
    name = factory.Faker('name') # TODO

    book = factory.SubFactory(BookFactory)


