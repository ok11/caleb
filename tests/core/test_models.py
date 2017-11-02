from faker import Faker
from testtools import TestCase
from testtools.matchers import Equals

from app import db, create_app
from tests.core.factories import *


class BaseTest(TestCase):

    def setUp(self):
        super().setUp()
        self.fake = Faker()
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        super().tearDown()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()



class TestBooks(BaseTest):

    def setUp(self):
        super(TestBooks, self).setUp()

    def tearDown(self):
        super(TestBooks, self).tearDown()

    def test_new_book_has_proper_attributes(self):
        book = BookFactory.build(title="Title")
        book.save()
        self.assertThat(book.title, Equals("Title"))

    def test_create_book_increases_books_count(self):
        count = len(Book.query.all())
        BookFactory.create(
            authors=(
                AuthorFactory.create(), AuthorFactory.create()
            )
        )
        self.assertThat(len(Book.query.all()), Equals(count + 1))

    def test_delete_book_decreases_books_count(self):
        book = BookFactory.create()
        count = len(Book.query.all())
        book.delete()
        self.assertThat(len(Book.query.all()), Equals(count - 1))

    def test_update_book_changes_its_attributes(self):
        book = BookFactory.create()
        title = self.fake.word()
        book.title = title
        book.save()
        self.assertThat(book.title, Equals(title))

    def test_get_book_retrieves_proper_attributes(self):
        new_book = BookFactory.create()
        id = new_book.id
        book = Book.query.get(id)
        self.assertThat(book.title, Equals(new_book.title))

    def test_get_book_returns_the_full_list(self):
        BookFactory.create()
        BookFactory.create()
        self.assertThat(len(Book.query.all()), Equals(2))

class TestAuthors(BaseTest):

    def setUp(self):
        super(TestAuthors, self).setUp()

    def tearDown(self):
        super(TestAuthors, self).tearDown()

    def test_new_author_has_proper_attributes(self):
        name = self.fake.name()
        author = AuthorFactory.create(name=name)
        self.assertThat(author.name, Equals(name))

    def test_create_author_increases_authors_count(self):
        count = len(Author.query.all())
        AuthorFactory.create()
        self.assertThat(len(Author.query.all()), Equals(count + 1))

    def test_delete_author_decreases_authors_count(self):
        count = len(Author.query.all())
        author = AuthorFactory.create()
        author.delete()
        self.assertThat(len(Author.query.all()), Equals(count))
