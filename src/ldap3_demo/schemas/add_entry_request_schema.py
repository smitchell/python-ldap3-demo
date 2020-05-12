from marshmallow import Schema, fields, post_load

from ldap3_demo.dtos.add_entry_request import AddEntryRequest
from ldap3_demo.schemas.attribute_schema import AttributeSchema


class AddEntryRequestSchema(Schema):
    dn = fields.Str()
    object_class = fields.Str()
    attributes = fields.List(fields.Nested(AttributeSchema), required=True)

    @post_load
    def create_add_entry_request(self, data, **kwargs):
        return AddEntryRequest(**data)