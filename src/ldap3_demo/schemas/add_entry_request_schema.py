from marshmallow import Schema, fields, post_load

from ldap3_demo.dtos.add_entry_request import AddEntryRequest
from ldap3_demo.schemas.key_value_pair_schema import KeyValuePairSchema


class AddEntryRequestSchema(Schema):
    dn = fields.Str()
    object_class = fields.Str()
    attributes = fields.List(fields.Nested(KeyValuePairSchema), required=True)

    @post_load
    def create_add_entry_request(self, data, **kwargs):
        return AddEntryRequest(**data)