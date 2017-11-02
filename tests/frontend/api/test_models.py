from faker import Faker
from testtools import TestCase
from testtools.matchers import Equals
from testtools.matchers import Contains

from app.frontend.api.model import *
from tests.frontend.api.factories import *

class TestDTO(TestCase):

    def setUp(self):
        super().setUp()
        self.fake = Faker()

    def tearDown(self):
        super().tearDown()

class TestBookDTO(TestDTO):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_created_book_renders_proper_attributes_to_json(self):
        title = self.fake.sentence()
        book = BookDTOFactory(title=title)
        self.assertThat(book.to_json(), Contains(title))

    def test_creation(self):
        title = self.fake.sentence()
        book = BookDTOFactory(title=title)
        self.assertThat(book.to_json(), Contains(title))

class TestAuthorDTO(TestCase): pass

class TestRatingDTO(TestCase): pass

class TestIdentifierDTO(TestCase): pass
