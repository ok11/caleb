from .model import *


class DataMapper:

    def schema(self, model):

        if isinstance(model, Book):
            return BookSchema(model)
        elif isinstance(model, Author):
            return AuthorSchema(model)
        elif isinstance(model, Identifier):
            return IdentifierSchema(model)
        elif isinstance(model, Comment):
            return CommentSchema(model)
        else:
            raise Exception('Unknown model')

    def model(self, schema):

        if isinstance(schema, BookSchema):
            return Book(**(schema.dump()))
        elif isinstance(schema, AuthorSchema):
            return Author(**(schema.dump()))
        elif isinstance(schema, IdentifierSchema):
            return Identifier(**(schema.dump()))
        elif isinstance(schema, CommentSchema):
            return Comment(**(schema.dump()))
        else:
            raise Exception('Unknown schema')
