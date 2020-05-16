#!/usr/bin/env python3
from ldap3.utils.conv import escape_filter_chars
from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load

from ldap3_demo.dtos.modify_entry_request import ModifyEntryRequest


class ModifyEntryRequestSchema(Schema):
    dn = fields.Str()
    changes = fields.Dict(
        keys=fields.Str(),
        values=fields.List(fields.Dict(keys=fields.Str(), values=fields.List(fields.Str()))), required=True)
    controls = fields.Dict(keys=fields.Str(), values=fields.Str(), allow_none=True)

    def convert_dict_to_tuple(self, changes):
        for attribute_key in changes:
            attribute = changes[attribute_key]
            temp_dict = {}
            result = []
            for operation in attribute:
                for operation_key in operation.keys():
                    if operation_key in temp_dict:
                        temp_dict[operation_key] += operation[operation_key]
                    else:
                        temp_dict[operation_key] = operation[operation_key]

            for key in temp_dict.keys():
                result.append(tuple([key] + temp_dict[key]))
            changes[attribute_key] = result

    @post_load
    def create_add_entry_request(self, data, **kwargs):
        self.convert_dict_to_tuple(data['changes'])
        return ModifyEntryRequest(**data)
