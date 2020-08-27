from marshmallow import Schema, fields


class AuthSchema(Schema):
    consumer_key = fields.Str(required=True)
    consumer_secret = fields.Str(required=True)
    grant_type = fields.Str(required=True, default="client_credentials")
    env = fields.Str(required=True, default="sandbox")


class LipaPayment(Schema):
    BusinessShortCode = fields.Int(required=True)
    Password = fields.Str(required=True)
    Amount = fields.Int(required=True)
    PartyA = fields.Str(required=True)
    PartyB = fields.Str(required=True)
    PhoneNumber = fields.Str(required=True)
    CallBackURL = fields.Str(required=True)
    AccountReference = fields.Str(required=True)
    TransactionDesc = fields.Str(required=True)
    TransactionType = fields.Str(required=True, default="CustomerPayBillOnline")
    Timestamp = fields.Str(required=True)


class LipaQuery(Schema):
    BusinessShortCode = fields.Int(required=True)
    Password = fields.Str(required=True)
    Timestamp = fields.Str(required=True)
    CheckoutRequestID = fields.Str(required=True)
