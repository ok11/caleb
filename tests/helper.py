import random
import uuid

from faker import Faker
from faker.providers import BaseProvider

fake = Faker()


class CalebProvider(BaseProvider):
    def lang_code(self):
        lang_code = fake.language_code()
        return lang_code

    def ebook_id_type(self):
        id_types = ('isbn', 'amazon')
        return random.choice(id_types)

    def ebook_id_value(self, **kwargs):
        id_type = kwargs.get('ebook_id_type', 'isbn')
        if id_type == 'isbn':
            val = fake.isbn13()
        else:
            val = uuid.uuid4()
        return str(val)

    def ebook_format(self):
        ebook_formats = ('pdf', 'fb2', 'epub', 'mobi')
        return random.choice(ebook_formats)
