from faker import Faker
from testtools import TestCase
from testtools.matchers import Equals

from app import create_app
from app.frontend.api.helper import *
from tests.core.factories import *


class BaseTest(TestCase):

    def setUp(self):
        super(BaseTest, self).setUp()
        self.fake = Faker()
        self.mapper = DataMapper()

    def tearDown(self):
        super(BaseTest, self).tearDown()


class TestDataMapper(BaseTest):

    def setUp(self):
        super(TestDataMapper, self).setUp()

    def tearDown(self):
        super(TestDataMapper, self).tearDown()

    def test_map_bookdb_to_bookdto(self):
        title = self.fake.sentence()
        bookdb = BookFactory.build(title=title)
        bookdto = self.mapper.bookdto(bookdb)
        self.assertThat(bookdto.title, Equals(title))

