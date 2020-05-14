from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load
from ldap3_demo.dtos.add_entry_request import AddEntryRequest


class AddEntryRequestSchema(Schema):
    dn = fields.Str()
    object_class = fields.Raw(required=True)
    attributes = fields.Dict(keys=fields.Str(), values=fields.Str(), allow_none=True)
    controls = fields.Dict(keys=fields.Str(), values=fields.Str(), allow_none=True)

    @post_load
    def create_add_entry_request(self, data, **kwargs):
        return AddEntryRequest(**data)
