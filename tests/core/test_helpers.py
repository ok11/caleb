import json
from testtools import TestCase
from testtools.matchers import *
from app.core.model import Dictable
from app.core.helper import DictableEncoder

class T1(Dictable):
    def __init__(self, **kwargs):
        self.c = kwargs.get('c', {})
        self.d = 'd'

    def to_dict(self):
        return {
            'c': self.c
        }


class T2:
    a = [1, 2, 3]
    b = T1(**{'c': {'e': ['f'], 'g': {'h': []}}})

    def __init__(self, **kwargs):
        self.c = kwargs.get('c', {})
        self.d = 'd'


class TestEncoder(TestCase):

    def setUp(self):
        super().setUp()
        self.encoder = DictableEncoder()

    def tearDown(self):
        super().tearDown();

    def test_encode(self):
        t2 = T2(**{'c': {'i': 1}})
        t3 = self.encoder.encode(t2)

        self.assertThat(t3, Contains(self.encoder.encode(t2.c)))
