from marshmallow import fields, validates, validate, ValidationError
from app.data import ma

class AuthorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'sort', 'link', '_links')

    id = fields.String(dump_only=True)
    link = fields.Url(required=False)
    _links = ma.Hyperlinks({
        'self': ma.UrlFor('api.get_author', id='<id>')
    })


class PublisherSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'sort', '_links')

    id = fields.String(dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.UrlFor('api.get_publisher', id='<id>')
    })

class IdentifierSchema(ma.Schema):
    class Meta:
        fields = ('id', 'type', 'val')

    id = fields.String(dump_only=True)

    @validates('type')
    def validate_type(self, type):
        types = ("amazon", "isbn", "doi", "goodreads", "douban", "google", "kobo", "ozon")
        if type not in types:
            raise ValidationError("Invalid value for identifier type: {}".format(type))


class TagSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')

    id = fields.String(dump_only=True)


class LanguageSchema(ma.Schema):
    class Meta:
        fields = ('id', 'lang_code')

    id = fields.String(dump_only=True, validate=validate.Regexp('[a-z][a-z]'))


class CommentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'text', '_links')

    id = fields.String(dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.UrlFor('api.get_comment', id='<id>')
    })


class BookSchema(ma.Schema):
    class Meta:
        fields = (
            'id', 'title', 'sort', 'author_sort',
            'pubdate', 'series_index', 'path', 'has_cover',
            'authors', 'languages', 'tags', 'publishers', 'identifiers',
            'timestamp', 'last_modified', '_links'
        )

    id = fields.String(dump_only=True)
    series_index = fields.Integer()
    timestamp = fields.DateTime(dump_only=True)
    last_modified = fields.DateTime(dump_only=True)
    authors = fields.Nested(AuthorSchema, only=('name', 'link'), many=True)
    languages = fields.Nested(LanguageSchema, many=True)
    tags = fields.Nested(TagSchema, only=('name'), many=True)
    identifiers = fields.Nested(IdentifierSchema, only=('type', 'val'), many=True)
    publishers = fields.Nested(PublisherSchema, only=('name'), many=True)
    _links = ma.Hyperlinks({
         'self': ma.UrlFor('api.get_book', id='<id>')
    }, dump_only=True)


