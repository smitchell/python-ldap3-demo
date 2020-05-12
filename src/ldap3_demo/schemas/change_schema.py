from flask_marshmallow import Schema
from marshmallow import fields

from ldap3_demo.schemas.operation_schema import OperationSchema


class ChangeSchema(Schema):
    attribute: fields.Str()
    changes: fields.List(fields.Nested(OperationSchema), required=True)
