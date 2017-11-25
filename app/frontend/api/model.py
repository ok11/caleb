from datetime import datetime

from marshmallow import fields, validates, validate, ValidationError, post_dump, utils, validates_schema

from app.data import ma


class BaseSchema(ma.Schema):
    class Meta:
        abstract = True

    @validates_schema
    def id_or_attrs(self, data):
        if 'id' in data and len(data.keys()) > 1:
            raise ValidationError('There should not be ID and attributes at the same time')


class AuthorSchema(BaseSchema):
    class Meta:
        fields = ('id', 'name', 'sort', 'link', '_links')

    id = fields.String(required=False, allow_none=False)
    link = fields.Url(required=False)
    _links = ma.Hyperlinks({
        'self': ma.UrlFor('api.get_author', id='<id>')
    }, dump_only=True)



class PublisherSchema(BaseSchema):
    class Meta:
        fields = ('id', 'name', 'sort', '_links')

    id = fields.String(required=False, allow_none=False)
    _links = ma.Hyperlinks({
        'self': ma.UrlFor('api.get_publisher', id='<id>')
    }, dump_only=True)


class IdentifierSchema(BaseSchema):
    class Meta:
        fields = ('id', 'type', 'val')

    id = fields.String(dump_only=True)

    @validates('type')
    def validate_type(self, type):
        types = ("amazon", "isbn", "doi", "goodreads", "douban", "google", "kobo", "ozon")
        if type not in types:
            raise ValidationError("Invalid value for identifier type: {}".format(type))


class TagSchema(BaseSchema):
    class Meta:
        fields = ('id', 'name')

    id = fields.String(required=False, allow_none=False)
    name = fields.String(required=True)


class SeriesSchema(BaseSchema):
    class Meta:
        fields = ('id', 'name', 'sort', '_links')

    id = fields.String(required=False, allow_none=False)
    name = fields.String(required=True)
    sort = fields.String(required=False)
    _links = ma.Hyperlinks({
        'self': ma.UrlFor('api.get_series', id='<id>')
    }, dump_only=True)


class LanguageSchema(BaseSchema):
    class Meta:
        fields = ('id', 'lang_code')

    id = fields.String(required=False, allow_none=False)
    lang_code = fields.String(required=True, validate=validate.Regexp('[a-z][a-z]'))


class CommentSchema(BaseSchema):
    class Meta:
        fields = ('id', 'text', '_links')

    id = fields.String(required=False, allow_none=False)
    _links = ma.Hyperlinks({
        'self': ma.UrlFor('api.get_comment', id='<id>')
    }, dump_only=True)


class BookSchema(BaseSchema):
    class Meta:
        fields = (
            'id', 'title', 'sort', 'author_sort',
            'pubdate', 'series_index', 'path', 'has_cover',
            'authors', 'languages', 'tags', 'publishers',
            'identifiers', 'series',
            'timestamp', 'last_modified', '_links'
        )

    id = fields.String(required=False, allow_none=False)
    series_index = fields.Integer()
    timestamp = fields.String(dump_only=True)
    last_modified = fields.String(dump_only=True)

    authors = fields.Nested(AuthorSchema, only=('name', 'link'), many=True, required=False)
    languages = fields.Nested(LanguageSchema, many=True, required=False)
    tags = fields.Nested(TagSchema, only=('name'), many=True, required=False)
    identifiers = fields.Nested(IdentifierSchema, only=('type', 'val'), many=True, required=False)
    publishers = fields.Nested(PublisherSchema, only=('name'), many=True, required=False)
    series = fields.Nested(SeriesSchema, only=('name'), many=True, required=False)

    _links = ma.Hyperlinks({
        'self': ma.UrlFor('api.get_book', id='<id>'),
        'collection': ma.UrlFor('api.get_books')
    }, dump_only=True)

    @post_dump()
    def timestamps(self, data):
        if data['timestamp']:
            ts = datetime.utcnow().strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
            data['timestamp'] = utils.isoformat(ts)
        if data['last_modified']:
            ts = datetime.utcnow().strptime(data['last_modified'], '%Y-%m-%d %H:%M:%S.%f')
            data['last_modified'] = utils.isoformat(ts)
