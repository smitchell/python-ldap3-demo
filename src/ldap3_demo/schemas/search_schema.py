#!/usr/bin/env python3

from marshmallow import Schema, fields, post_load
from marshmallow.validate import OneOf
from ldap3_demo.dtos.search import Search


class SearchSchema(Schema):
    search_base = fields.Str(required=True)
    search_filter = fields.Str(required=True)
    search_scope = fields.Str(default='SUBTREE', validate=OneOf(['BASE', 'LEVEL=LEVEL', 'SUBTREE']))
    dereference_aliases = fields.Str(default='DEREF_ALWAYS',
                                     validate=OneOf(['DEREF_NEVER', 'DEREF_SEARCH', 'DEREF_BASE', 'DEREF_ALWAYS']))
    attributes = fields.Raw(allow_none=True)
    size_limit = fields.Int()
    time_limit = fields.Int()
    types_only = fields.Bool()
    get_operational_attributes = fields.Bool()
    controls = fields.Dict(keys=fields.Str(), values=fields.Str(), allow_none=True)
    paged_size = fields.Int(allow_none=True)
    paged_criticality = fields.Bool()
    paged_cookie = fields.Str(allow_none=True)

    @post_load
    def create_search(self, data, **kwargs):
        return Search(**data)
