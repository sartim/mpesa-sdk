from marshmallow import Schema, fields


class AuthSchema(Schema):
    consumer_key = fields.Str(required=True)
    consumer_secret = fields.Str(required=True)
    grant_type = fields.Str(required=True, default="client_credentials")
    env = fields.Str(required=True, default="sandbox")


class LipaQuery(Schema):
    BusinessShortCode = fields.Str(required=True)
    Password = fields.Str(required=True)
    Timestamp = fields.Str(required=True)
    CheckoutRequestID = fields.Str(required=True)
