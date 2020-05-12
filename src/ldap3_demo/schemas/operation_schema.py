from marshmallow import Schema
from marshmallow import fields
from marshmallow.validate import OneOf

from ldap3_demo.dtos.change import Change

OPERATION_TYPES = [
    'MODIFY_ADD',
    'MODIFY_DELETE',
    'MODIFY_REPLACE',
    'MODIFY_INCREMENT'
]


class OperationSchema(Schema):
    operation_type = fields.Str(validate=OneOf(OPERATION_TYPES))
    changes = fields.List(fields.Str())
