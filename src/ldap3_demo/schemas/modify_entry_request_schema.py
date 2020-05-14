from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load

from ldap3_demo.dtos.modify_entry_request import ModifyEntryRequest


class ModifyEntryRequestSchema(Schema):
    dn = fields.Str()
    changes = fields.Dict(keys=fields.Str(),
                          values=fields.List(
                              fields.Dict(
                                  key=fields.Str(),
                                  values=fields.List(
                                      fields.Str()
                                  )
                              )
                          ),
                          required=True)
    controls = fields.Dict(keys=fields.Str(), values=fields.Str(), allow_none=True)

    @post_load
    def create_add_entry_request(self, data, **kwargs):
        return ModifyEntryRequest(**data)
