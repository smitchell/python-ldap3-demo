from marshmallow import Schema
from marshmallow import fields


class OperationSchema(Schema):
    operation_type = fields.Str()
    changes = fields.List(fields.Str())