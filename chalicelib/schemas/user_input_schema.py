from marshmallow import fields

from chalicelib.base_schema import BaseSchema


class UserInputSchema(BaseSchema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
