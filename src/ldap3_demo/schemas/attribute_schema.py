from marshmallow import Schema, fields, post_load

from ldap3_demo.dtos.attribute import Attribute


class AttributeSchema(Schema):
    name = fields.Str()
    value = fields.Str()

    @post_load
    def create_attribute(self, data, **kwargs):
        return Attribute(**data)



