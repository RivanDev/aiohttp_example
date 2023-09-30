from marshmallow import Schema, fields

from app.web.schemes import OkResponseSchema


class UserSchema(Schema):
    email = fields.Str(required=True)


class UserGetRequestSchema(Schema):
    id = fields.UUID(required=True)


class UserGetSchema(Schema):
    user = fields.Nested(UserSchema)


class UserGetResponseSchema(OkResponseSchema):
    data = fields.Nested(UserGetSchema)


class ListUserSchema(Schema):
    users = fields.Nested(UserSchema, many=True)


class ListUsersResponseSchema(OkResponseSchema):
    data = fields.Nested(ListUserSchema)
