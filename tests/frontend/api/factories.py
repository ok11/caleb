import random
import factory

from faker import Faker

from faker.providers import BaseProvider

fake = Faker()

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

fake.add_provider(CalebProvider)

class Tag():
    name = fake('word')

    def to_json(self):
        json

class PublisherDTOFactory(factory.Factory):
    class Meta:
        model = PublisherDTO

    name = factory.Faker('company')
    sort = name


class LanguageDTOFactory(factory.Factory):
    class Meta:
        model = LanguageDTO

    lang_code = factory.Faker('lang_code')


class RatingDTOFactory(factory.Factory):
    class Meta:
        model = RatingDTO

    rating = factory.Faker('pyint')


class AuthorDTOFactory(factory.Factory):
    class Meta:
        model = AuthorDTO

    name = factory.Faker('name')
    sort = name
    link = factory.Faker('url')


class SeriesDTOFactory(factory.Factory):
    class Meta:
        model = SeriesDTO

    name = factory.Faker('word')
    sort = name


class BookDTOFactory(factory.Factory):
    class Meta:
        model = BookDTO

    title = factory.Faker('sentence', nb_words=3)
    sort = title
    author_sort = factory.Faker('name')
    timestamp = factory.Faker('iso8601')
    pubdate = factory.Faker('iso8601')
    series_index = factory.Faker('pyint')
    last_modified = factory.Faker('iso8601')
    path = factory.Faker('file_path', depth=2)
    has_cover = factory.Faker('boolean')

    authors = factory.SubFactory(AuthorDTOFactory)
    tags = factory.SubFactory(TagDTOFactory)
    languages = factory.SubFactory(LanguageDTOFactory)

class CommentDTOFactory(factory.Factory):
    class Meta:
        model = CommentDTO

    text = factory.Faker('sentence', nb_words=10)

    book = factory.SubFactory(BookDTOFactory)


class IdentifierDTOFactory(factory.Factory):
    class Meta:
        model = IdentifierDTO

    type = factory.Faker('ebook_id_type')
    val = factory.Faker('ebook_id_value', ebook_id_type=type)

    book = factory.SubFactory(BookDTOFactory)


class DataDTOFactory(factory.Factory):
    class Meta:
        model = DataDTO

    format = factory.Faker('ebook_format')
    uncompressed_size = factory.Faker('pyint')
    name = factory.Faker('name') # TODO

    book = factory.SubFactory(BookDTOFactory)


