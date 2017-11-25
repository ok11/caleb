from faker import Faker
from testtools import TestCase
from testtools.matchers import Equals

from app import create_app
from app.frontend.api.helper import *
from tests.core.factories import *


class BaseTest(TestCase):

    def setUp(self):
        super().setUp()
        self.fake = Faker()

    def tearDown(self):
        super().tearDown()

