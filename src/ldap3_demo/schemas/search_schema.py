from marshmallow import Schema, fields, post_load

from ldap3_demo.dtos.search import Search


class SearchSchema(Schema):
    search_base = fields.Str(required=True)
    search_filter = fields.Str(required=True)
    search_scope = fields.Str(required=True)
    dereference_aliases = fields.Str(required=True)
    attributes = fields.Str(allow_none=True)
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