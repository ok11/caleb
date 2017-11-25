import factory

from app.core.model import *

from faker import Faker

from tests.helper import CalebProvider

fake = Faker()

factory.Faker.add_provider(CalebProvider)


class BaseFactory(factory.Factory):
    class Meta:
        abstract = True

    id = factory.Sequence(lambda n: '%d' % n)


class IdFactory(BaseFactory): pass


class TagFactory(BaseFactory):
    class Meta:
        model = BaseTag

    name = factory.Faker('word')


class PublisherFactory(BaseFactory):
    class Meta:
        model = BasePublisher

    name = factory.Faker('company')


class LanguageFactory(BaseFactory):
    class Meta:
        model = BaseLanguage

    lang_code = factory.Faker('lang_code')


class RatingFactory(BaseFactory):
    class Meta:
        model = BaseRating

    rating = factory.Faker('pyint')


class AuthorFactory(BaseFactory):
    class Meta:
        model = BaseAuthor

    name = factory.Faker('name')
    sort = factory.SelfAttribute('name')
    link = factory.Faker('url')


class SeriesFactory(BaseFactory):
    class Meta:
        model = BaseSeries

    name = factory.Faker('word')
    sort = factory.SelfAttribute('name')


class BookFactory(BaseFactory):
    class Meta:
        model = BaseBook

    title = factory.Faker('sentence', nb_words=3)
    sort = title
    author_sort = factory.Faker('name')
    timestamp = datetime.strftime(fake.date_time(), '%Y-%m-%d %H:%M:%S.%f')
    pubdate = factory.Faker('iso8601')
    series_index = factory.Faker('pyint')
    last_modified = datetime.strftime(fake.date_time(), '%Y-%m-%d %H:%M:%S.%f')
    path = factory.Faker('file_path', depth=2)
    has_cover = factory.Faker('boolean')

    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        if extracted:
            for author in extracted:
                self.authors.append(author)

    @factory.post_generation
    def languages(self, create, extracted, **kwargs):
        if extracted:
            for language in extracted:
                self.languages.append(language)

    @factory.post_generation
    def identifiers(self, create, extracted, **kwargs):
        if extracted:
            for ident in extracted:
                self.identifiers.append(ident)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if extracted:
            for tag in extracted:
                self.tags.append(tag)


class CommentFactory(factory.Factory):
    class Meta:
        model = BaseComment

    text = factory.Faker('sentence', nb_words=10)

#    book = factory.SubFactory(BookFactory)


class IdentifierFactory(factory.Factory):
    class Meta:
        model = BaseIdentifier

    type = factory.Faker('ebook_id_type')
    val = factory.Faker('ebook_id_value', ebook_id_type=type)

#    book = factory.SubFactory(BookFactory)


class DataFactory(factory.Factory):
    class Meta:
        model = BaseData

    format = factory.Faker('ebook_format')
    uncompressed_size = factory.Faker('pyint')
    name = factory.Faker('name')

#    book = factory.SubFactory(BookFactory)


