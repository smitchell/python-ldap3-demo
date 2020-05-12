from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load
from ldap3_demo.dtos.modify_entry_request import ModifyEntryRequest
from ldap3_demo.schemas.change_schema import ChangeSchema


class ModifyEntryRequestSchema(Schema):
    dn = fields.Str()
    changes = fields.List(fields.Nested(ChangeSchema), required=True)
    controls = fields.Dict(keys=fields.Str(), values=fields.Str(), allow_none=True)

    @post_load
    def create_add_entry_request(self, data, **kwargs):
        return ModifyEntryRequest(**data)
