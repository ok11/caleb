import json

from app import create_app

from app.frontend.api.model import *
from tests.frontend.api.factories import *

from faker import Faker
from testtools import TestCase
from testtools.matchers import Equals
from testtools.matchers import Contains


class TestModel(TestCase):

    def setUp(self):
        super().setUp()
        self.fake = Faker()
        self.app = create_app(config_name="testing")
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        super().tearDown()
        self.app_context.pop()

class TestBook(TestModel):

    def setUp(self):
        super().setUp()
        self.book_schema = BookSchema()
        self.books_schema = BookSchema(many=True)

    def tearDown(self):
        super().tearDown()

    def test_dump_book_with_basic_attributes(self):
        title = self.fake.sentence()
        book = BookFactory.build(id='1', title=title)
        data = self.book_schema.dump(book)
        self.assertThat(json.dumps(data), Contains(title))

    def test_dump_book_with_associations(self):
        book = BookFactory.build(
            authors=[AuthorFactory.build(id='1')],
            identifiers=[IdentifierFactory.build(id='1')],
            tags=[TagFactory.build(id='1')],
            series=[SeriesFactory.build(id='1')]
        )
        data = self.book_schema.dump(book)
        self.assertThat(json.dumps(data), Contains('authors'))

class TestAuthor(TestModel): pass

class TestRating(TestModel): pass

class TestIdentifier(TestModel): pass
