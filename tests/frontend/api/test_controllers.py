import json
import datetime
import testtools

from faker import Faker
from testtools import TestCase
from testtools.matchers import Equals
from testtools.matchers import Contains
from testtools.matchers import Not
from testtools.matchers import Is

#from tests.frontend.api.factories import *

from app import create_app, db

from app.core.model import Book

from tests.core.factories import *
from app.frontend.api.model import *

book_schema = BookSchema()
fake = Faker()

class BooksAPITest(TestCase):
    """This class represents the books test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        super(BooksAPITest, self).setUp()

        self.fake = Faker()

        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Tear down all initialized variables."""
        super(BooksAPITest, self).tearDown()
        db.session.remove()
#        db.drop_all()
        self.app_context.pop()

    def test_book_creation_with_all_attributes_succeeds(self):
        """Test API creates a book (POST request) and returns 201 Created"""
        data = {
            "title": fake.word(),
            "sort": fake.word(),
            "author_sort": fake.name(),
            "pubdate": fake.date(),
            "series_index": fake.pyint(),
            "path": fake.file_path(depth=3),
            "has_cover": fake.boolean(),
            "authors": [{
                "name": fake.name(),
                "link": fake.url()
            }],
            "languages": [{
                "lang_code": "en"
            }],
            "identifiers": [{
                "type": "google",
                "val": "12345678"
            },{
                "type": "amazon",
                "val": "12345678"
            }],
            "tags": [{
                "val": "sf"
            }]
        }
        j = json.dumps(data)
        res = self.client().post(
            '/api/books/',
            content_type='application/json',
            data=j
        )
        self.assertThat(res.status_code, Equals(201))
        self.assertThat(str(res.data), Contains(data['title']))
        self.assertThat(res.headers['location'], Not(Is(None)))

    def test_book_creation_without_authors_succeeds(self):
        """Test API creates a book (POST request) and returns 201 Created"""
        data = {
            "title": fake.word(),
            "sort": fake.word(),
            "author_sort": fake.name(),
            "pubdate": fake.date(),
            "series_index": fake.pyint(),
            "path": fake.file_path(depth=3),
            "has_cover": fake.boolean(),
            "languages": [{
                "lang_code": "en"
            }],
            "identifiers": [{
                "type": "google",
                "val": "12345678"
            },{
                "type": "amazon",
                "val": "12345678"
            }],
            "tags": [{
                "val": "sf"
            }]
        }
        j = json.dumps(data)
        res = self.client().post(
            '/api/books/',
            content_type='application/json',
            data=j
        )
        self.assertThat(res.status_code, Equals(201))
        self.assertThat(str(res.data), Contains(data['title']))
        self.assertThat(res.headers['location'], Not(Is(None)))

    def test_book_creation_with_wrong_attributes_fails(self):
        """Test API creates a book (POST request) and returns JSON with its data"""
        data = {
            "title": fake.word(),
            "sort": fake.word(),
            "author_sort": fake.name(),
            "pubdate": fake.date(),
            "series_index": fake.pyint(),
            "path": fake.file_path(depth=3),
            "has_cover": fake.boolean(),
            "authors": [{
                "name": fake.name(),
                "link": fake.url()
            }],
            "languages": [{
                "name": "en" # fails
            }],
            "identifiers": [{
                "type": "google",
                "val": "12345678"
            },{
                "type": "amazon",
                "val": "12345678"
            }],
            "tags": [{
                "val": "sf"
            }]
        }
        j = json.dumps(data)
        res = self.client().post(
            '/api/books/',
            content_type='application/json',
            data=j
        )
        self.assertThat(res.status_code, Equals(400))

    def test_books_query_returns_200(self):
        """Test API gets a list of books (GET request) and returns 200 OK"""
        res = self.client().get('/api/books/', content_type='application/json')
        self.assertThat(res.status_code, Equals(200))

    def test_books_query_returns_all_books(self):
        """Test API gets a list of all books (GET request)"""
        BookFactory.create()
        res = self.client().get('/api/books/', content_type='application/json')
        books = json.loads(res.data)
        self.assertThat(len(list(books)), Equals(len(Book.query.all())))


# Make the tests conveniently executable
if __name__ == "__main__":
    testtools.main()
