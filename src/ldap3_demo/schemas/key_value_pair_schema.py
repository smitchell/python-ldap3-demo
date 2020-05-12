from marshmallow import Schema, fields, post_load

from ldap3_demo.dtos.key_value_pair import KeyValuePair


class KeyValuePairSchema(Schema):
    key = fields.Str()
    value = fields.Str()

    @post_load
    def create_attribute(self, data, **kwargs):
        return KeyValuePair(**data)



